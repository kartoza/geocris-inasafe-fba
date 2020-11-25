# coding=utf-8
from rest_framework.views import APIView, Response
from fba.models.all import HazardEvent
from fba.serializers.hazard_event import HazardEventSerializer


class RecentHazardList(APIView):
    """API for listing 5 most recent hazard"""

    def get(self, request):
        hazard_events = HazardEvent.objects.all().order_by(
            '-forecast_date', '-acquisition_date'
        )[:5]
        hazard_event_serializer = HazardEventSerializer(
            hazard_events,
            many=True
        )
        return Response(hazard_event_serializer.data)
