from rest_framework import serializers

from fba.models.views import (
    BuildingSummaryDistrictStats,
    BuildingSummarySubDistrictStats,
    CensusPopulationSummaryDistrictStats,
    CensusPopulationSummarySubDistrictStats, RoadSummaryDistrictStats,
    RoadSummarySubDistrictStats)


class BuildingSummaryDistrictSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    district_id = serializers.SerializerMethodField()

    def get_name(self, obj: BuildingSummaryDistrictStats):
        return obj.district.name

    def get_district_id(self, obj: BuildingSummaryDistrictStats):
        return obj.district.id

    class Meta:
        model = BuildingSummaryDistrictStats
        fields = '__all__'
        # exclude = [
        #     'id',
        #     'hazard_event',
        #     'district',
        #     'trigger_status'
        # ]


class BuildingSummarySubDistrictSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    sub_district_id = serializers.SerializerMethodField()

    def get_name(self, obj: BuildingSummarySubDistrictStats):
        return obj. sub_district.name

    def get_sub_district_id(self, obj: BuildingSummarySubDistrictStats):
        return obj.sub_district.id

    class Meta:
        model = BuildingSummarySubDistrictStats
        fields = '__all__'
        # exclude = [
        #     'id',
        #     'hazard_event',
        #     'district',
        #     'sub_district',
        #     'trigger_status'
        # ]


class RoadSummaryDistrictSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    district_id = serializers.SerializerMethodField()

    def get_name(self, obj: RoadSummaryDistrictStats):
        return obj.district.name

    def get_district_id(self, obj: RoadSummaryDistrictStats):
        return obj.district.id

    class Meta:
        model = RoadSummaryDistrictStats
        fields = '__all__'
        # exclude = [
        #     'id',
        #     'hazard_event',
        #     'district',
        #     'trigger_status'
        # ]


class RoadSummarySubDistrictSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    sub_district_id = serializers.SerializerMethodField()

    def get_name(self, obj: RoadSummarySubDistrictStats):
        return obj. sub_district.name

    def get_sub_district_id(self, obj: RoadSummarySubDistrictStats):
        return obj.sub_district.id

    class Meta:
        model = RoadSummarySubDistrictStats
        fields = '__all__'
        # exclude = [
        #     'id',
        #     'hazard_event',
        #     'district',
        #     'sub_district',
        #     'trigger_status'
        # ]


class CensusPopulationSummaryDistrictSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    district_id = serializers.SerializerMethodField()

    def get_name(self, obj: CensusPopulationSummaryDistrictStats):
        return obj. district.name

    def get_district_id(self, obj: CensusPopulationSummaryDistrictStats):
        return obj.district.id

    class Meta:
        model = CensusPopulationSummaryDistrictStats
        fields = '__all__'
        # exclude = [
        #     'id',
        #     'hazard_event',
        #     'district',
        #     'trigger_status'
        # ]


class CensusPopulationSummarySubDistrictSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    sub_district_id = serializers.SerializerMethodField()

    def get_name(self, obj: CensusPopulationSummarySubDistrictStats):
        return obj. sub_district.name

    def get_sub_district_id(self, obj: CensusPopulationSummarySubDistrictStats):
        return obj.sub_district.id

    class Meta:
        model = CensusPopulationSummarySubDistrictStats
        fields = '__all__'
        # exclude = [
        #     'id',
        #     'hazard_event',
        #     'district',
        #     'sub_district',
        #     'trigger_status'
        # ]
