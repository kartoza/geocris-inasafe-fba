from rest_framework import serializers

from fba.models.all import (
    HazardEvent, HazardMap, HazardType)


class HazardEventSerializer(serializers.Serializer):
    """
    Serializer for hazard event model.
    """
    id = serializers.IntegerField(read_only=True)
    hazard_map = serializers.SerializerMethodField()
    hazard_type = serializers.SerializerMethodField()

    def get_hazard_type(self, obj):
        try:
            hazard_type = HazardType.objects.get(
                id=obj.hazard_type_id
            )
            return hazard_type.name
        except HazardType.DoesNotExist:
            return '-'

    def get_hazard_map(self, obj):
        try:
            hazard_map = HazardMap.objects.get(
                id=obj.flood_map_id
            )
            return HazardMapSerializer(hazard_map).data
        except HazardMap.DoesNotExist:
            return '-'

    class Meta:
        model = HazardEvent
        fields = (
            'id',
            'source',
            'notes',
            'forecast_date',
            'acquisition_date',
            'link',
            'hazard_type',
            'trigger_status',
            'hazard_map'
        )


class HazardMapSerializer(serializers.ModelSerializer):
    """
    Serializer for hazard map model
    """
    class Meta:
        model = HazardMap
        fields = (
            'notes',
            'place_name'
        )
