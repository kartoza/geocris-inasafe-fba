#!/usr/bin/env python3
import os

from utils import GeoServerRESTRunner


def create_styles(runner, session, style_name):

    response = runner.assert_get(
        session,
        '/workspaces/kartoza/styles/{style_name}.json'.format(
            style_name=style_name))

    if not response.ok:
        data = {
            'style': {
                'name': style_name,
                'format': 'sld',
                # 'languageVersion': {
                #     'version': '1.1.0'
                # },
                'filename': '{style_name}.sld'.format(
                    style_name=style_name)
            }
        }

        response = runner.assert_post(
            session,
            '/workspaces/kartoza/styles',
            json=data,
            validate=True
        )

    # Check if style body already exists
    response = runner.assert_get(
        session,
        '/workspaces/kartoza/styles/{style_name}.sld'.format(
            style_name=style_name))

    if response.ok and response.text.strip():
        print('SLD Style already exits')
        return response

    sld_path = os.path.join(
        os.path.dirname(__file__),
        'sld/{style_name}.sld'.format(
            style_name=style_name))

    with open(sld_path) as f:
        data = f.read()

    response = runner.assert_put(
        session,
        '/workspaces/kartoza/styles/{style_name}'.format(
            style_name=style_name),
        data=data,
        headers={
            'Content-type': 'application/vnd.ogc.sld+xml'
        }
    )

    runner.print_response(response)

    return response


if __name__ == '__main__':

    runner = GeoServerRESTRunner()
    with runner.session() as s:

        styles = [
            'red_outline',
            'building_vulnerability',
            'exposed_roads',
            'hazard_class',
            'osm_buildings',
            'osm_roads',
            'osm_waterways_scale',
            'district_map',
            'sub_district_map',
            'village_map',
            'osm_admin_web',
            'BlueprintBuildings',
            'BlueprintRoads',
            'BlueprintRivers',
        ]

        for style in styles:
            response = create_styles(runner, s, style)
            if not response.ok:
                break

        exit(not response.ok)
