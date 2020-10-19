import logging

from django import test

from fba.models.hazard_event import HazardEvent
from fba.models.views import HazardEventExtent
from fba.serializers.common import SpatialExtentSerializer
from fba.serializers.hazard_event import HazardEventSerializer


logger = logging.getLogger(__name__)


class TestHazardEventSerializer(test.LiveServerTestCase):

    databases = ['default', 'backend']

    def test_hazard_serializer(self):
        model_objs = HazardEvent.objects.all()
        objects = HazardEventSerializer(model_objs, many=True)
        logger.debug(objects.data)

        # extent
        target_id = model_objs[0].id
        extent_obj = HazardEventExtent.objects.get(id=target_id)
        object = SpatialExtentSerializer(extent_obj)
        logger.debug(object.data)
