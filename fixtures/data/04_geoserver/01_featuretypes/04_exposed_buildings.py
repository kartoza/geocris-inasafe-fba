#!/usr/bin/env python3
import os

from utils import GeoServerRESTRunner

if __name__ == '__main__':

    runner = GeoServerRESTRunner()
    with runner.session() as s:

        response = runner.assert_get(
            s,
            '/workspaces/kartoza/datastores/gis/featuretypes/exposed_buildings')

        if response.ok:
            print('Resource exists.')
            print()
            exit(0)

        data = {
            'featureType': {
                'name': 'exposed_buildings',
                'nativeName': 'mv_hazard_event_buildings',
                'title': 'Hazard Event Buildings Map',
                'srs': 'EPSG:4326',
                'abstract': 'This layer shows the buildings for a given hazard event. It is intended that you use a CQL filter passing the hazard_event_id when using this layer.',
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
                },
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
