#!/usr/bin/env python3
import os

from utils import GeoServerRESTRunner

if __name__ == '__main__':

    runner = GeoServerRESTRunner()
    with runner.session() as s:

        response = runner.assert_get(
            s,
            '/workspaces/kartoza/datastores/gis/featuretypes/hazard_forecast_layer')

        if response.ok:
            print('Resource exists.')
            print()
            exit(0)

        data = {
            'featureType': {
                'name': 'hazard_forecast_layer',
                'nativeName': 'hazard_forecast_layer',
                'title': 'Hazard Forecast Map',
                'srs': 'EPSG:4326',
                'abstract': 'This layer shows the hazard extent for a given hazard event. It is intended that you use a CQL filter passing the id when using this layer.',
                'metadata': {
                    'entry': [
                        {
                            '@key': 'JDBC_VIRTUAL_TABLE',
                            'virtualTable': {
                                'name': 'hazard_forecast_layer',
                                'sql': """select 
                                row_number() OVER () AS gid,
                                hazard_event.id as id,
                                geometry,
                                hazard_class
                                from hazard_event
                                inner join hazard_map on hazard_event.hazard_map_id = hazard_map.id
                                inner join hazard_areas on hazard_map.id = hazard_areas.hazard_map_id
                                inner join hazard_area on hazard_areas.hazarded_area_id = hazard_area.id""",
                                'escapeSql': False,
                                'geometry': {
                                    'name': 'geometry',
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
