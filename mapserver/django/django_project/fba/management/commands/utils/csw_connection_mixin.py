import re

import requests
from owslib.csw import CatalogueServiceWeb, CswRecord
from owslib.fes import PropertyIsLike


class BoundaryCSWConnectionMixin:

    def create_connection(self):
        csw = CatalogueServiceWeb('https://geocris2.cdema.org/catalog/')
        self._response_cache = None
        return csw

    def session_get(self, url):
        if self._response_cache and self._response_cache['url'] == url:
            return self._response_cache['response']
        response = requests.get(url)
        self._response_cache = {
            'url': url,
            'response': response
        }
        return response

    def get_table_header(self, conn: CatalogueServiceWeb, schema_name, table_name):
        datasource_filter = PropertyIsLike('dc:source', table_name)
        conn.getrecords2(constraints=[datasource_filter], esn='full')
        record: CswRecord = [r for r in conn.records.values()][0]
        wfs_ref = [
            ref for ref
            in record.references if ref['scheme'] == 'OGC:OAPIF'][0]
        # This is a direct GeoJSON url
        response = self.session_get(wfs_ref['url'])
        geojson = response.json()
        props: dict = geojson['features'][0]['properties']
        return [k for k in props.keys()] + ['geom']

    def get_admin_data(self, conn, schema_name, table_name):
        datasource_filter = PropertyIsLike('dc:source', table_name)
        conn.getrecords2(constraints=[datasource_filter], esn='full')
        record: CswRecord = [r for r in conn.records.values()][0]
        wfs_ref = [
            ref for ref
            in record.references if ref['scheme'] == 'OGC:OAPIF'][0]
        # This is a direct GeoJSON url
        response = self.session_get(wfs_ref['url'])
        geojson = response.json()
        values = []
        table_header = self.get_table_header(conn, schema_name, table_name)
        for feature in geojson['features']:
            props = feature['properties']
            row = [
                props[header] for header in table_header if not header == 'geom'
            ] + [feature['geometry']]
            values.append(row)
        return values

    def get_all_tables(self, conn: CatalogueServiceWeb, schema):
        datasource_filter = PropertyIsLike('dc:source', f'{schema}_bnd_adm%')
        conn.getrecords2(constraints=[datasource_filter], esn='full')
        scheme_pattern = r'features/collections/(?P<schema>[a-z]{3})\.(?P<table>\w+)/items\.json'
        table_list = []
        startpos = 0
        while True:
            for key in conn.records:
                record: CswRecord = conn.records[key]
                try:
                    wfs_ref = [
                        ref for ref
                        in record.references if ref['scheme'] == 'OGC:OAPIF'][0]
                    match = re.search(scheme_pattern, wfs_ref['url'])
                    if match:
                        table_list.append(record.source)
                except:
                    pass
                startpos += 1
            # Fetch next page
            if conn.results['nextrecord'] == 0:
                break
            conn.getrecords2(
                constraints=[datasource_filter],
                startposition=startpos,
                esn='full')
        return table_list

    def get_all_schemas(self, conn: CatalogueServiceWeb):
        administrative_record_filter = PropertyIsLike('csw:AnyText', 'Administrative Boundary')
        conn.getrecords2(constraints=[administrative_record_filter], esn='full')
        scheme_pattern = r'features/collections/(?P<schema>[a-z]{3})\.(?P<table>\w+)/items\.json'
        schemas_set = set()
        startpos = 0
        while True:
            for key in conn.records:
                record: CswRecord = conn.records[key]
                try:
                    wfs_ref = [
                        ref for ref
                        in record.references if ref['scheme'] == 'OGC:OAPIF'][0]
                    match = re.search(scheme_pattern, wfs_ref['url'])
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
                startposition=startpos,
                esn='full')
        return list(schemas_set)
