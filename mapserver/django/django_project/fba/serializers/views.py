from rest_framework import serializers

from fba.models.views import (
    BuildingSummaryDistrictStats,
    BuildingSummarySubDistrictStats,
    CensusPopulationSummaryDistrictStats,
    CensusPopulationSummarySubDistrictStats)


class BuildingSummaryDistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = BuildingSummaryDistrictStats
        fields = '__all__'


class BuildingSummarySubDistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = BuildingSummarySubDistrictStats
        fields = '__all__'


class CensusPopulationSummaryDistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = CensusPopulationSummaryDistrictStats
        fields = '__all__'


class CensusPopulationSummarySubDistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = CensusPopulationSummarySubDistrictStats
        fields = '__all__'
