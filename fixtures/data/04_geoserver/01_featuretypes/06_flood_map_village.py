#!/usr/bin/env python3
import os

from utils import GeoServerRESTRunner

if __name__ == '__main__':

    runner = GeoServerRESTRunner()
    with runner.session() as s:

        response = runner.assert_get(
            s,
            '/workspaces/kartoza/datastores/gis/featuretypes/hazard_map_village')

        if response.ok:
            print('Resource exists.')
            print()
            exit(0)

        data = {
            'featureType': {
                'name': 'hazard_map_village',
                'nativeName': 'hazard_map_village',
                'title': 'hazard_map_village',
                'srs': 'EPSG:4326',
                'metadata': {
                    'entry': [
                        {
                            '@key': 'JDBC_VIRTUAL_TABLE',
                            'virtualTable': {
                                'name': 'hazard_map_village',
                                'sql': """
                                select row_number() OVER () AS id,a.hazard_event_id,
                                a.district_id,a.name,a.trigger_status,
                                b.geom 
                                from 
                                mv_hazard_event_village_summary a  
                                join village b on b.village_code = a.village_id""",
                                'escapeSql': False,
                                'geometry': {
                                    'name': 'geom',
                                    'type': 'MultiPolygon',
                                    'srid': 4326
                                }
                            }
                        },
                    ]
                },
                'nativeBoundingBox': {
                    'minx': -180,
                    'maxx': 180,
                    'miny': -90,
                    'maxy': 90,
                    'crs': 'EPSG:4326'
                },
                'latLonBoundingBox': {
                    'minx': -180,
                    'maxx': 180,
                    'miny': -90,
                    'maxy': 90,
                    'crs': 'EPSG:4326'
                }
            }
        }

        response = runner.assert_post(
            s,
            '/workspaces/kartoza/datastores/gis/featuretypes/',
            json=data,
            validate=True
        )

        runner.print_response(response)

        exit(not response.ok)
