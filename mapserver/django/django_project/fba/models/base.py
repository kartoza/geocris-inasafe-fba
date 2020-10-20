__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '11/06/20'

from django.contrib.gis.db import models


class base_model(models.Model):
    _DATABASE = 'backend'

    class Meta:
        abstract = True
