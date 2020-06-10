__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '09/06/20'

import json
import os
import requests
from urllib.parse import unquote
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest


def getSLDStyle(layer_name):
    """ return sld style in json
    :param layer_name: the layer name that needs to be checked
    :return:
    """
    fixture_file = os.path.join(settings.FIXTURES, 'data', 'layer_style.json')
    with open(fixture_file, 'r') as _file:
        sld = json.load(_file).get(layer_name, None)
        if sld:
            return os.path.join(settings.MAPSERVER_PUBLIC_SLD_URL, sld)
    return None


def wms(request):
    try:
        if request.method == 'GET':
            params = unquote(request.build_absolute_uri().split('?')[1].lower())
            params = params.replace('kartoza:', '')
            if 'GetMap' == request.GET.get('request', None):
                layers = request.GET['layers'] if 'layers' in request.GET else request.GET['LAYERS']
                layers = layers.replace('kartoza:', '')
                sld = getSLDStyle(layers)
                if sld:
                    params += '&sld=' + sld
            mapserver_url = '{}?{}'.format(settings.MAPSERVER_PUBLIC_WMS_URL, params)
            response = requests.get(mapserver_url)
            return HttpResponse(
                content=response.content,
                status=response.status_code,
                content_type=response.headers['Content-Type']
            )
        else:
            return HttpResponseForbidden(
                'Method is forbidden')
    except KeyError as e:
        return HttpResponseBadRequest(
            '{} is needed'.format(e))
