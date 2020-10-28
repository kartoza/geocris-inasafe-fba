import requests
import json
from datetime import datetime
from django.core.management.base import BaseCommand
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

    def handle(self, *args, **options):
        self.request_data()

    def request_data(self):
        """Request data from geocris pg-featureserv"""
        forecast_cone_url = (
            '{base_url}/noaa/collections/noaa.coneforecastal202020/items.json?limit={limit}'.format(
                base_url=self.base_url,
                limit=self.limit
            )
        )

        print('Request forecast cones...')
        response = requests.get(forecast_cone_url)
        item_data = response.json()

        # Hazard type
        hazard_type, _ = HazardType.objects.get_or_create(
            name='Hurricane - NOAA'
        )

        unique_storm_ids = []

        print('Get unique ids')
        for feature in item_data['features']:
            properties = feature['properties']
            if properties['ncstormid'] not in unique_storm_ids:
                unique_storm_ids.append(properties['ncstormid'])

        print('Fetch latest storms')
        # Get the latest hazard event from storm_id
        for unique_storm_id in unique_storm_ids:
            latest_cone_url = (
                '{base_url}/noaa/collections/noaa.coneforecastal202020/items.json?orderBy=validtime:D&limit=1&ncstormid={id}'.format(
                    base_url=self.base_url,
                    id=unique_storm_id
                )
            )
            response = requests.get(latest_cone_url)
            latest_cone_data = response.json()

            latest_points_url = (
                '{base_url}/noaa/collections/noaa.centerpositionforecastal202020/items.json?validtime={validtime}&orderBy=ogc_fid'.format(
                    base_url=self.base_url,
                    validtime=latest_cone_data['features'][0]['properties']['validtime']
                )
            )

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

            hazard, created = HazardEvent.objects.get_or_create(
                forecast_date=start_time_obj,
                acquisition_date=ref_time_obj,
                hazard_map_id=hazard_map.id,
                hazard_type_id=hazard_type.id,
                link=latest_cone_data_prop['url'],
                source=latest_cone_data_prop['url'],
                notes='valid_time:{validtime}'.format(
                    **latest_cone_data_prop
                )
            )

            print('Hazard Event Created = {}'.format(created))
