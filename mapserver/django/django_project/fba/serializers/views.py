from rest_framework import serializers

from fba.models.views import (
    BuildingSummaryDistrictStats,
    BuildingSummarySubDistrictStats,
    CensusPopulationSummaryDistrictStats,
    CensusPopulationSummarySubDistrictStats, RoadSummaryDistrictStats,
    RoadSummarySubDistrictStats, BuildingSummaryCountryStats,
    RoadSummaryCountryStats, CensusPopulationSummaryCountryStats)


class BuildingSummaryCountrySerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    country_id = serializers.SerializerMethodField()

    def get_name(self, obj: BuildingSummaryCountryStats):
        return obj.country.name

    def get_country_id(self, obj: BuildingSummaryCountryStats):
        return obj.country.id

    class Meta:
        model = BuildingSummaryCountryStats
        fields = '__all__'


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


class RoadSummaryCountrySerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    country_id = serializers.SerializerMethodField()

    def get_name(self, obj: RoadSummaryCountryStats):
        return obj.country.name

    def get_country_id(self, obj: RoadSummaryCountryStats):
        return obj.country.id

    class Meta:
        model = RoadSummaryCountryStats
        fields = '__all__'


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


class CensusPopulationSummaryCountrySerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    country_id = serializers.SerializerMethodField()

    def get_name(self, obj: CensusPopulationSummaryCountryStats):
        return obj. country.name

    def get_country_id(self, obj: CensusPopulationSummaryCountryStats):
        return obj.country.id

    class Meta:
        model = CensusPopulationSummaryCountryStats
        fields = '__all__'


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
