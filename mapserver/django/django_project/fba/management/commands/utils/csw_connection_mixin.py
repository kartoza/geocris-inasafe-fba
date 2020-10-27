import re

import requests
from owslib.csw import CatalogueServiceWeb, CswRecord
from owslib.fes import PropertyIsLike


class BoundaryCSWConnectionMixin:

    def create_connection(self):
        csw = CatalogueServiceWeb('https://geocris2.cdema.org/catalog/')
        return csw

    def get_table_header(self, conn: CatalogueServiceWeb, schema_name, table_name):
        datasource_filter = PropertyIsLike('dc:source', table_name)
        conn.getrecords2(constraints=[datasource_filter])
        record: CswRecord = conn.records[0]
        wfs_ref = [
            ref for ref
            in record.references if ref['scheme'] == 'OGC:OAPIF'][0]
        # This is a direct GeoJSON url
        response = requests.get(wfs_ref)
        geojson = response.json()
        props: dict = geojson['features'][0]['properties']
        return props.keys()

    def get_admin_data(self, conn, schema_name, table_name):
        datasource_filter = PropertyIsLike('dc:source', table_name)
        conn.getrecords2(constraints=[datasource_filter])
        record: CswRecord = conn.records[0]
        wfs_ref = [
            ref for ref
            in record.references if ref['scheme'] == 'OGC:OAPIF'][0]
        # This is a direct GeoJSON url
        response = requests.get(wfs_ref['url'])
        geojson = response.json()
        values = []
        table_header = self.get_table_header(conn, schema_name, table_name)
        for feature in geojson['features']:
            props = feature['properties']
            row = [
                props[header] for header in table_header
            ]
            values.append(row)
        return values

    def get_all_tables(self, conn: CatalogueServiceWeb, schema):
        datasource_filter = PropertyIsLike('dc:source', f'{schema}_bnd_adm%')
        conn.getrecords2(constraints=[datasource_filter])
        table_list = []
        for key in conn.records:
            record: CswRecord = conn.records[key]
            table_list.append(record.source)
        return table_list

    def get_all_schemas(self, conn: CatalogueServiceWeb):
        administrative_record_filter = PropertyIsLike('csw:AnyText', 'Administrative Boundary')
        conn.getrecords2(constraints=[administrative_record_filter])
        schema_pattern = r'features/collections/(?P<schema>[a-z]{3})\.(?P<table>\w+)/items\.json'
        schemas_set = set()
        startpos = 0
        while True:
            for key in conn.records:
                record: CswRecord = conn.records[key]
                try:
                    wfs_ref = [
                        ref for ref
                        in record.references if ref['scheme'] == 'OGC:OAPIF'][0]
                    match = re.search(schema_pattern, wfs_ref['url'])
                    if match:
                        schema_name = match.group('schema')
                        schemas_set.add(schema_name)
                except:
                    pass
                startpos += 1
            # Fetch next page
            if conn.results['nextrecord'] == 0:
                break
            conn.getrecords2(
                constraints=[administrative_record_filter],
                startposition=startpos)
        return list(schemas_set)
