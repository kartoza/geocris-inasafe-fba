import datetime

from rest_framework import serializers

from fba.models.all import (
    HazardEvent, HazardMap, HazardType)


class HazardEventSerializer(serializers.ModelSerializer):
    """
    Serializer for hazard event model.
    """
    hazard_map = serializers.SerializerMethodField()
    hazard_type = serializers.SerializerMethodField()
    lead_time = serializers.SerializerMethodField()
    is_historical = serializers.SerializerMethodField()

    def get_lead_time(self, obj: HazardEvent) -> int:
        return (obj.forecast_date - obj.acquisition_date).days

    def get_is_historical(self, obj: HazardEvent) -> bool:
        return obj.forecast_date <= datetime.datetime.utcnow()

    def get_hazard_type(self, obj: HazardEvent):
        try:
            hazard_type = obj.hazard_type
            return hazard_type.name
        except HazardType.DoesNotExist:
            return '-'

    def get_hazard_map(self, obj: HazardEvent):
        try:
            hazard_map = obj.hazard_map
            return HazardMapSerializer(hazard_map).data
        except HazardMap.DoesNotExist:
            return '-'

    class Meta:
        model = HazardEvent
        fields = '__all__'


class HazardMapSerializer(serializers.ModelSerializer):
    """
    Serializer for hazard map model
    """
    class Meta:
        model = HazardMap
        fields = '__all__'
