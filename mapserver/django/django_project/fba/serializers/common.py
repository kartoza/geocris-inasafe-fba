from rest_framework import serializers


class SpatialExtentSerializer(serializers.BaseSerializer):

    id = serializers.IntegerField(read_only=True)
    x_min = serializers.FloatField()
    y_min = serializers.FloatField()
    x_max = serializers.FloatField()
    y_max = serializers.FloatField()

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'x_min': instance.x_min,
            'y_min': instance.y_min,
            'x_max': instance.x_max,
            'y_max': instance.y_max
        }
