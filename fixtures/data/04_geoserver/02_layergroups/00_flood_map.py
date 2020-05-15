#!/usr/bin/env python3
import os

from utils import GeoServerRESTRunner

if __name__ == '__main__':

    runner = GeoServerRESTRunner()
    with runner.session() as s:

        response = runner.assert_get(
            s,
            '/workspaces/kartoza/layergroups/hazard_map')

        if response.ok:
            print('Resource exists.')
            print()
            exit(0)

        data = {
            'layerGroup': {
                'name': 'hazard_map',
                'mode': 'SINGLE',
                'title': 'hazard map',
                'publishables': {
                    'published': [
                        {
                            '@type': 'layer',
                            'name': 'hazard_map_district',
                        },
                        {
                            '@type': 'layer',
                            'name': 'hazard_map_sub_district',
                        },
                        {
                            '@type': 'layer',
                            'name': 'hazard_map_village',
                        }
                    ]
                },
                'styles': {
                    'style': [
                        {
                            'name': 'district_map',
                        },
                        {
                            'name': 'sub_district_map',
                        },
                        {
                            'name': 'village_map',
                        }
                    ]
                },
                'bounds': {
                    'minx': -180,
                    'maxx': 180,
                    'miny': -90,
                    'maxy': 90,
                    'crs': 'EPSG:4326'
                },
            }
        }

        response = runner.assert_post(
            s,
            '/workspaces/kartoza/layergroups/',
            json=data,
            validate=True
        )

        runner.print_response(response)

        exit(not response.ok)
