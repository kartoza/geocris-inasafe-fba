import re

from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand
from django.db import connections
from osgeo import ogr

from fba.management.commands.utils.csw_connection_mixin import \
    BoundaryCSWConnectionMixin
from fba.models.all import (
    District, Country, SubDistrict, Village, Census,
    AdminBoundaryGlobalKeyMapping)


class Command(BaseCommand, BoundaryCSWConnectionMixin):
    """ Command to process first hazard event queue. """
    base_url = 'https://geocris2.cdema.org/'
    limit = 10

    def generate_admin_code(self, schema_name, adm_level, origin_id):
        partition_names = ['country', 'district', 'sub_district', 'village']
        partition_name = partition_names[adm_level]

        try:
            last_obj = AdminBoundaryGlobalKeyMapping.objects.filter(
                partition_level=adm_level).order_by('-id_mapping').first()
            last_id = last_obj.id_mapping + 1
        except:
            last_id = 1

        admin_code_name = f'{schema_name}:{adm_level}:{origin_id}'

        data = {
            'key': admin_code_name,
            'partition_level': adm_level,
            'defaults': {
                'id_mapping': last_id,
                'partition': partition_name,
            }
        }

        key_mapping, created = AdminBoundaryGlobalKeyMapping.objects.get_or_create(
            **data)

        return key_mapping.id_mapping

    def get_last_id(self, ModelClass):
        try:
            return ModelClass.objects.order_by('-id').first().id + 1
        except:
            return 1

    def assign_admin_hierarchy(self):
        with connections['backend'].cursor() as cursor:
            cursor.execute('select kartoza_fba_assign_admin_hierarchy()')

    def handle(self, *args, **options):
        conn = self.create_connection()
        schema_names = self.get_all_schemas(conn)

        layer_pattern = re.compile(
            r'^(?P<schema>.*)_bnd_adm(?P<adm_level>\d+)'
            r'_(?P<is_population>(pop_)?)polygon$')

        for schema_name in sorted(schema_names):
            table_names = self.get_all_tables(conn, schema_name)
            table_names = sorted(table_names)
            table_names = [t for t in table_names if layer_pattern.match(t)]

            # Check if tables have more than one level of population data
            # We only need the most detail one.
            last_pop_level = None
            chosen_pop_table = None
            _filtered_table_names = []
            for t in table_names:
                matches = layer_pattern.match(t)
                adm_level = int(matches.group('adm_level'))
                has_pop_column = bool(matches.group('is_population'))
                if has_pop_column and last_pop_level is None:
                    last_pop_level = adm_level
                    chosen_pop_table = t
                    continue
                elif has_pop_column and adm_level - last_pop_level > 0:
                    last_pop_level = adm_level
                    chosen_pop_table = t
                    continue
                _filtered_table_names.append(t)
            if chosen_pop_table:
                table_names = _filtered_table_names + [chosen_pop_table]
            else:
                table_names = _filtered_table_names

            for table_name in table_names:
                matches = layer_pattern.match(table_name)
                adm_level = int(matches.group('adm_level'))
                # If it is the last boundary level. Assume random pop
                # for now
                has_pop_column = bool(matches.group('is_population')) \
                    or table_name == table_names[-1]

                target_table_mapping = [
                    'country', 'district', 'sub_district', 'village']

                rows = self.get_admin_data(conn, schema_name, table_name)
                header = self.get_table_header(conn, schema_name, table_name)

                # Prepare common variables
                Models = {
                    'country': Country,
                    'district': District,
                    'sub_district': SubDistrict,
                    'village': Village
                }
                admin_code_key = {
                    'country': 'country_code',
                    'district': 'dc_code',
                    'sub_district': 'sub_dc_code',
                    'village': 'village_code'
                }

                # Table exists, get name, pop and geometry
                print(f'Table name {table_name}')
                for row in rows:
                    target_table_name = target_table_mapping[adm_level]
                    geometry = None
                    if f'adm{adm_level}' in header:
                        name = row[header.index(f'adm{adm_level}')]
                    elif f'name_{adm_level}' in header:
                        name = row[header.index(f'name_{adm_level}')]
                    elif 'name' in header:
                        name = row[header.index('name')]
                    elif 'parish' in header:
                        name = row[header.index('parish')]
                    elif 'loc_name' in header:
                        name = row[header.index('loc_name')]
                    elif 'comm_name' in header:
                        name = row[header.index('comm_name')]
                    elif 'identifica' in header:
                        name = row[header.index('identifica')]
                    else:
                        if 'district' in header:
                            name = row[header.index('district')]
                        else:
                            name = '{schema}_{id}'.format(
                                schema=schema_name,
                                id=row[0]
                            )

                    name = name.strip() if name else ''

                    if has_pop_column:
                        pop_column = [c for c in header if 'pop' in c]
                        try:
                            pop = row[header.index(pop_column[0])]
                        except IndexError:
                            pop = 0

                    if 'geom' in header:
                        geometry = row[header.index('geom')]

                    origin_key = [c for c in header if c in ['id', 'ogc_fid']][0]
                    origin_id = row[header.index(origin_key)]

                    # if it has geometry, update admin boundary tables
                    if geometry:
                        geojson = geometry.geojson if hasattr(geometry, 'geojson') else geometry
                        geom = GEOSGeometry(str(geojson))

                        if not geom.ogr.geom_type == 'MultiPolygon':
                            # Flatten non 2D geometry
                            g = ogr.CreateGeometryFromWkt(geom.wkt)
                            g.FlattenTo2D()
                            geom = GEOSGeometry(g.ExportToWkt())

                        ModelClass = Models[target_table_name]

                        admin_code = self.generate_admin_code(
                            schema_name, adm_level, origin_id)

                        try:
                            data = {
                                admin_code_key[target_table_name]: admin_code,
                                'defaults': {
                                    'id': self.get_last_id(ModelClass),
                                    'geom': geom,
                                    'name': name,
                                }
                            }
                            boundary, created = ModelClass.objects.get_or_create(
                                **data)
                            if not created:
                                del data['defaults']['id']
                                ModelClass.objects.update_or_create(**data)

                            print(f'{target_table_name.capitalize()} '
                                  f'{schema_name} - {name} = {created}')
                        except Exception as e:
                            print(str(e))
                            raise e

                    # If it has population column, must update census table
                    if has_pop_column:
                        if adm_level != 3:
                            # population data is not on village level.
                            # Interpolate/Assume/Use current level to the
                            # lower level
                            for level in range(adm_level + 1, 4):
                                target_table_name = target_table_mapping[level]
                                ModelClass = Models[target_table_name]
                                admin_code = self.generate_admin_code(
                                    schema_name, level, origin_id)
                                data = {
                                    admin_code_key[
                                        target_table_name]: admin_code,
                                    'defaults': {
                                        'id': self.get_last_id(ModelClass),
                                        'geom': geom,
                                        'name': name
                                    }
                                }
                                boundary, created = ModelClass.objects.get_or_create(
                                    **data)
                                if not created:
                                    del data['defaults']['id']
                                    ModelClass.objects.update_or_create(**data)

                        # boundary must now refer to village level
                        # insert population data to census table
                        data = {
                            'village_id': boundary.village_code,
                            'defaults': {
                                'population': pop
                            }
                        }
                        census_entry, created = Census.objects.update_or_create(
                            **data)

        self.assign_admin_hierarchy()
