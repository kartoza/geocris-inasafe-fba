from rest_framework import serializers

from fba.models.all import (
    HazardEvent, HazardMap, HazardType)


class HazardEventSerializer(serializers.ModelSerializer):
    """
    Serializer for hazard event model.
    """
    hazard_map = serializers.SerializerMethodField()
    hazard_type = serializers.SerializerMethodField()

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
