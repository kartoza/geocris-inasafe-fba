from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView

from fba.models.hazard_event import HazardEvent
from fba.models.views import HazardEventExtent
from fba.serializers.common import SpatialExtentSerializer
from fba.serializers.hazard_event import HazardEventSerializer


class HazardEventAPI(viewsets.ModelViewSet):
    """API for listing hazard event"""

    queryset = HazardEvent.objects.all()
    serializer_class = HazardEventSerializer
    ordering_fields = ['-forecast_date']


class HazardEventExtentAPI(RetrieveAPIView):

    lookup_field = 'id'
    queryset = HazardEventExtent
    serializer_class = SpatialExtentSerializer
