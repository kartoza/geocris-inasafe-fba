# coding=utf-8

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from mapserver.api.wms import wms

urlpatterns = [
    url(r'^wms', wms, name='wms'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'image/png'])
