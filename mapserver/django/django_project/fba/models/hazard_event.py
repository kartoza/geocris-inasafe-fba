__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '11/06/20'

from django.contrib.gis.db import models

from fba.models.base import base_model


class HazardEvent(base_model):
    """ Model for hazard event queue """
    id = models.AutoField(primary_key=True)
    hazard_map = models.ForeignKey('HazardMap', models.DO_NOTHING,
                                   db_column='flood_map_id', blank=True,
                                   null=True)
    acquisition_date = models.DateTimeField()
    forecast_date = models.DateTimeField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    trigger_status = models.ForeignKey('TriggerStatus', models.DO_NOTHING,
                                       db_column='trigger_status', blank=True,
                                       null=True)
    progress = models.IntegerField(blank=True, null=True)
    hazard_type = models.ForeignKey('HazardType', models.DO_NOTHING,
                                    db_column='hazard_type_id', blank=True,
                                    null=True)

    class Meta:
        managed = False
        db_table = 'hazard_event'

    def __str__(self):
        return '{source} - {date}'.format(
            source=self.source,
            date=self.acquisition_date
        )
