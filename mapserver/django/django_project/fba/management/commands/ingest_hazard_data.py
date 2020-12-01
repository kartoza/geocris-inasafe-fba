import requests
import re
import json
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import connections
from django.utils.timezone import make_aware
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from fba.models.all import HazardArea, HazardMap, HazardAreas, HazardClass, HazardType
from fba.models.hazard_event import HazardEvent
from fba.scripts.cone_divider import ConeDivider


class Command(BaseCommand):
    """ Command to process first hazard event queue. """
    base_url = 'https://geocris2.cdema.org/'
    limit = 10
    storm_type = {
        'MH': 'Major Hurricane (Category 3 -5)',
        'HU': 'Hurricane (Category 1 -2)',
        'TS': 'Tropical Storm',
        'STS': 'Subtropical Storm',
        'TD': 'Tropical Depression',
    }

    def add_arguments(self, parser):
        parser.add_argument('storm_ids', nargs='*', type=str)
        parser.add_argument(
            '--validtime',
            dest='validtime',
            type=int)

    def handle(self, *args, storm_ids=None, validtime=None, **options):
        self.request_data(unique_storm_ids=storm_ids, validtime=validtime)

    def recalculate_impact(self, hazard):
        with connections['backend'].cursor() as cursor:
            cursor.execute('select kartoza_process_hazard_event_queue()')
            cursor.execute('select kartoza_calculate_impact()')
            cursor.execute(f'select kartoza_fba_generate_excel_report_for_flood({hazard.id})')

    def request_data(self, unique_storm_ids=None, validtime=None):
        """Request data from geocris pg-featureserv"""
        if not unique_storm_ids:
            # Fetch active storm endpoint
            active_storm_url = f'{self.base_url}/noaa/functions/active_storms/items.json'
            print('Request active storms...')
            response = requests.get(active_storm_url)
            try:
                storm_tables = response.json()
            except:
                # No active storms currently
                print('No active storms...')
                exit(0)

            # Get all latest storm ids
            cone_forecast_pattern = re.compile(
                r'coneforecast(?P<storm_id>.*)')

            unique_storm_ids = set()
            for table in storm_tables:
                match = cone_forecast_pattern.search(table['_table_name'])
                if match:
                    storm_id = match.group('storm_id')
                    unique_storm_ids.add(storm_id)
                    print(f'Found latest storm id: {storm_id}')

        # Hazard type
        hazard_type, _ = HazardType.objects.get_or_create(
            name='Hurricane NOAA'
        )

        print('Fetch latest storms')
        # Get the latest hazard event from storm_id
        for unique_storm_id in list(unique_storm_ids):
            print(f'Processing storm id: {unique_storm_id}')

            if not validtime:
                # find latest
                latest_cone_url = (
                    f'{self.base_url}/noaa/collections/noaa.coneforecast{unique_storm_id}'
                    f'/items.json?orderBy=validtime:D&limit=1'
                )
            else:
                # filter by time
                latest_cone_url = (
                    f'{self.base_url}/noaa/collections/noaa.coneforecast'
                    f'{unique_storm_id}'
                    f'/items.json?validtime={validtime}'
                )
            print(f'Fetch cone URL: {latest_cone_url}')
            response = requests.get(latest_cone_url)
            latest_cone_data = response.json()
            validtime = latest_cone_data['features'][0]['properties']['validtime']
            cone_fid = latest_cone_data['features'][0]['id']

            latest_points_url = (
                f'{self.base_url}/noaa/collections'
                f'/noaa.centerpositionforecast{unique_storm_id}'
                f'/items.json?validtime={validtime}&orderBy=ogc_fid'
            )

            print(f'Fetch points url: {latest_points_url}')

            response = requests.get(latest_points_url)
            latest_points_data = response.json()

            # Divide the cone by points
            print('Split cones')
            cone_divider = ConeDivider(
                points=latest_points_data,
                cone_json=latest_cone_data
            )
            cones = cone_divider.split_cones()
            print('Result : {} cones'.format(len(cones['features'])))

            hazard_map = None

            # Create hazard area for each cone
            for cone in cones['features']:
                properties = cone['properties']

                # Hazard class
                if properties['stormtype'] not in self.storm_type:
                    storm_type = properties['tcdvlp']
                else:
                    storm_type = self.storm_type[properties['stormtype']]
                hazard_classes = HazardClass.objects.filter(
                    label=storm_type,
                    hazard_type=hazard_type
                )

                if not hazard_classes.exists():
                    all_hazard_class = [h for h in HazardClass.objects.all()]
                    hazard_class_last_id = all_hazard_class[-1].id + 1
                    hazard_class, _ = HazardClass.objects.get_or_create(
                        label=storm_type,
                        hazard_type=hazard_type,
                        id=hazard_class_last_id
                    )
                else:
                    hazard_class = hazard_classes[0]

                # Hazard area
                geometry = GEOSGeometry(json.dumps(cone['geometry']))
                hazard_area, _ = HazardArea.objects.get_or_create(
                    geometry=MultiPolygon(geometry),
                    depth_class=hazard_class
                )

                # Hazard map
                hazard_map, _ = HazardMap.objects.get_or_create(
                    notes='valid_time:{validtime}'.format(
                        validtime=properties['validtime']
                    ),
                    place_name=properties['stormname']
                )

                # Hazard areas
                HazardAreas.objects.get_or_create(
                    hazard_map=hazard_map,
                    impacted_area=hazard_area
                )

            latest_cone_data_prop = latest_cone_data['features'][0]['properties']

            # Hazard event
            start_time = str(latest_cone_data_prop['starttime'])
            start_time = int(start_time[:-3])
            start_time_obj = datetime.fromtimestamp(start_time)
            start_time_obj = make_aware(start_time_obj)

            ref_time = str(latest_cone_data_prop['reftime'])
            ref_time = int(ref_time[:-3])
            ref_time_obj = datetime.fromtimestamp(ref_time)
            ref_time_obj = make_aware(ref_time_obj)

            hazard_source_link = (
                f'{self.base_url}/noaa/collections'
                f'/noaa.coneforecast{unique_storm_id}'
                f'/items.html?ogc_fid={cone_fid}')

            hazard, created = HazardEvent.objects.get_or_create(
                forecast_date=start_time_obj,
                acquisition_date=ref_time_obj,
                hazard_map_id=hazard_map.id,
                hazard_type_id=hazard_type.id,
                link=hazard_source_link,
                source=latest_cone_data_prop['url'],
                notes='valid_time:{validtime}'.format(
                    **latest_cone_data_prop
                )
            )

            print(f'Hazard Event Created = {created}')
            print(f'Hazard Event id = {hazard.id}')

            self.recalculate_impact(hazard)
