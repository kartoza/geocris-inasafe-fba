from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand
from django.db import connections
from osgeo import ogr

from fba.management.commands.utils.csw_connection_mixin import \
    (
    RoadCSWConnectionMixin)
from fba.models.all import (
    RoadGlobalKeyMapping, OsmRoads)


class Command(BaseCommand, RoadCSWConnectionMixin):
    """ Command to process first hazard event queue. """
    base_url = 'https://geocris2.cdema.org/'
    limit = 10

    def generate_road_code(self, schema_name, table_name, origin_id):
        try:
            last_obj = RoadGlobalKeyMapping.objects.order_by('-id_mapping').first()
            last_id = last_obj.id_mapping + 1
        except:
            last_id = 1

        admin_code_name = f'{schema_name}:{table_name}:{origin_id}'

        data = {
            'key': admin_code_name,
            'defaults': {
                'id_mapping': last_id,
            }
        }

        key_mapping, created = RoadGlobalKeyMapping.objects.get_or_create(
            **data)

        return key_mapping.id_mapping

    def get_last_id(self, ModelClass):
        try:
            return ModelClass.objects.order_by('-id').first().id + 1
        except:
            return 1

    def recalculate_impact(self):
        with connections['backend'].cursor() as cursor:
            cursor.execute('select kartoza_evaluate_road_admin()')
            cursor.execute('select kartoza_calculate_impact()')

    def handle(self, *args, **options):
        conn = self.create_connection()
        schema_names = self.get_all_schemas(conn)

        for schema_name in sorted(schema_names):
            table_names = self.get_all_tables(conn, schema_name)
            table_names = sorted(table_names)

            for table_name in table_names:

                try:
                    rows = self.get_admin_data(conn, schema_name, table_name)
                    header = self.get_table_header(conn, schema_name, table_name)
                except:
                    # If failed to fetch data, continue
                    print(f'Failed to fetch data from {schema_name} {table_name}')
                    continue

                # Table exists, get name, pop and geometry
                print(f'Table name {table_name}')
                for row in rows:
                    geometry = None
                    name = None
                    if 'name' in header:
                        name = row[header.index('name')]

                    name = name.strip() if name else ''

                    if 'geom' in header:
                        geometry = row[header.index('geom')]

                    origin_key = [c for c in header if c in ['id', 'ogc_fid']][0]
                    origin_id = row[header.index(origin_key)]

                    # if it has geometry, update admin boundary tables
                    if geometry:
                        geojson = geometry.geojson if hasattr(geometry, 'geojson') else geometry
                        geom = GEOSGeometry(str(geojson))

                        if not str(geom.ogr.geom_type).lower() in ['linestring', 'multilinestring']:
                            # Only handle lines
                            print('Will only handle linestring or multilinestring')
                            continue

                        if not geom.ogr.geom_type == 'LineString':
                            # Flatten non 2D geometry
                            g = ogr.CreateGeometryFromWkt(geom.wkt)
                            line = ogr.ForceToLineString(g)
                            geom = GEOSGeometry(line.ExportToWkt())

                        ModelClass = OsmRoads

                        admin_code = self.generate_road_code(
                            schema_name, table_name, origin_id)

                        try:
                            data = {
                                'osm_id': admin_code,
                                'defaults': {
                                    'id': self.get_last_id(ModelClass),
                                    'geometry': geom,
                                    'name': name,
                                }
                            }
                            entry, created = ModelClass.objects.get_or_create(
                                **data)
                            if not created:
                                del data['defaults']['id']
                                ModelClass.objects.update_or_create(**data)

                            print(f'{table_name.capitalize()} '
                                  f'{schema_name} - {admin_code} - {name} = {created}')
                        except Exception as e:
                            print(str(e))
                            raise e

        self.recalculate_impact()
