from django.contrib.gis.db import models
from fba.models.base import base_model


class HazardEventExtent(base_model):
    """Model for hazard extent view"""

    id = models.IntegerField(primary_key=True)
    x_min = models.FloatField()
    y_min = models.FloatField()
    x_max = models.FloatField()
    y_max = models.FloatField()

    class Meta:
        managed = False
        db_table = 'vw_hazard_event_extent'
