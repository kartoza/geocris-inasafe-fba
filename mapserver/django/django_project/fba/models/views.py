from django.contrib.gis.db import models
from django.db.models.aggregates import Sum
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet

from fba.models.all import District, SubDistrict, Country
from fba.models.base import base_model
from fba.models.hazard_event import HazardEvent


class HazardEventExtent(base_model):
    """Model for hazard extent view"""

    id = models.IntegerField(primary_key=True)
    x_min = models.FloatField()
    y_min = models.FloatField()
    x_max = models.FloatField()
    y_max = models.FloatField()

    class Meta:
        managed = False
        db_table = 'vw_hazard_event_extent'


class AdministrativeMapping(base_model):
    """Model for administrative mapping"""

    country_id = models.IntegerField()
    country_name = models.CharField(max_length=255)
    district_id = models.IntegerField()
    district_name = models.CharField(max_length=255)
    sub_district_id = models.IntegerField()
    sub_district_name = models.CharField(max_length=255)
    village_id = models.IntegerField()
    village_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'mv_administrative_mapping'


class CountryFilterQuerySet(QuerySet):

    def filter(self, **kwargs):
        filter_args = kwargs
        if 'country_id' in filter_args:
            country_id = filter_args.get('country_id')
            del filter_args['country_id']
            filter_args['district__country__country_code'] = country_id
        return super().filter(**filter_args)


CountryFilterManager = CountryFilterQuerySet.as_manager


class BaseSummaryStats(base_model):

    hazard_event = models.ForeignKey(HazardEvent, models.DO_NOTHING,
                                     db_column='flood_event_id', blank=True,
                                     null=True)
    trigger_status = models.ForeignKey('TriggerStatus', models.DO_NOTHING,
                                       db_column='trigger_status', blank=True,
                                       null=True)

    class Meta:
        abstract = True

    @classmethod
    def aggregate_stats_by(cls, **kwargs):
        # infer field lists
        fields: [models.FloatField] = [f for f in cls._meta.fields if isinstance(f, models.FloatField)]
        aggregate_mapping = {
            f.name: Sum(f.name) for f in fields
        }
        return cls.objects.all().filter(**kwargs).aggregate(
            **aggregate_mapping)


class BaseBuildingSummaryStats(BaseSummaryStats):

    building_count = models.FloatField()
    impacted_building_count = models.FloatField(db_column='flooded_building_count')
    total_vulnerability_score = models.FloatField()
    # impacted count
    residential_impacted_building_count = models.FloatField(db_column='residential_flooded_building_count')
    clinic_dr_impacted_building_count = models.FloatField(db_column='clinic_dr_flooded_building_count')
    fire_station_impacted_building_count = models.FloatField(db_column='fire_station_flooded_building_count')
    school_impacted_building_count = models.FloatField(db_column='school_flooded_building_count')
    university_impacted_building_count = models.FloatField(db_column='university_flooded_building_count')
    government_impacted_building_count = models.FloatField(db_column='government_flooded_building_count')
    hospital_impacted_building_count = models.FloatField(db_column='hospital_flooded_building_count')
    police_station_impacted_building_count = models.FloatField(db_column='police_station_flooded_building_count')
    supermarket_impacted_building_count = models.FloatField(db_column='supermarket_flooded_building_count')
    sports_facility_impacted_building_count = models.FloatField(db_column='sports_facility_flooded_building_count')
    # not impacted count
    residential_building_count = models.FloatField()
    clinic_dr_building_count = models.FloatField()
    fire_station_building_count = models.FloatField()
    school_building_count = models.FloatField()
    university_building_count = models.FloatField()
    government_building_count = models.FloatField()
    hospital_building_count = models.FloatField()
    police_station_building_count = models.FloatField()
    supermarket_building_count = models.FloatField()
    sports_facility_building_count = models.FloatField()

    class Meta:
        abstract = True


class BuildingSummaryCountryStats(BaseBuildingSummaryStats):

    country = models.ForeignKey(Country, models.DO_NOTHING,
                                 db_column='country_id', blank=True,
                                 null=True)

    class Meta:
        managed = False
        db_table = 'mv_flood_event_country_summary'


class BuildingSummaryDistrictStats(BaseBuildingSummaryStats):

    district = models.ForeignKey(District, models.DO_NOTHING,
                                 db_column='district_id', blank=True,
                                 null=True)

    objects = CountryFilterManager()

    class Meta:
        managed = False
        db_table = 'mv_flood_event_district_summary'


class BuildingSummarySubDistrictStats(BaseBuildingSummaryStats):

    district = models.ForeignKey(District, models.DO_NOTHING,
                                 db_column='district_id', blank=True,
                                 null=True)
    sub_district = models.ForeignKey(SubDistrict, models.DO_NOTHING,
                                     db_column='sub_district_id', blank=True,
                                     null=True)

    class Meta:
        managed = False
        db_table = 'mv_flood_event_sub_district_summary'


class BaseRoadSummaryStats(BaseSummaryStats):

    road_count = models.FloatField()
    impacted_road_count = models.FloatField(db_column='flooded_road_count')
    total_vulnerability_score = models.FloatField()
    # impacted count
    track_impacted_road_count = models.FloatField(db_column='track_flooded_road_count')
    motorway_highway_impacted_road_count = models.FloatField(db_column='motorway_highway_flooded_road_count')
    motorway_link_impacted_road_count = models.FloatField(db_column='motorway_link_flooded_road_count')
    tertiary_link_impacted_road_count = models.FloatField(db_column='tertiary_link_flooded_road_count')
    secondary_link_impacted_road_count = models.FloatField(db_column='secondary_link_flooded_road_count')
    primary_link_impacted_road_count = models.FloatField(db_column='primary_link_flooded_road_count')
    tertiary_impacted_road_count = models.FloatField(db_column='tertiary_flooded_road_count')
    secondary_impacted_road_count = models.FloatField(db_column='secondary_flooded_road_count')
    primary_impacted_road_count = models.FloatField(db_column='primary_flooded_road_count')
    residential_impacted_road_count = models.FloatField(db_column='residential_flooded_road_count')
    # not impacted count
    track_road_count = models.FloatField()
    motorway_highway_road_count = models.FloatField()
    motorway_link_road_count = models.FloatField()
    tertiary_link_road_count = models.FloatField()
    secondary_link_road_count = models.FloatField()
    primary_link_road_count = models.FloatField()
    tertiary_road_count = models.FloatField()
    secondary_road_count = models.FloatField()
    primary_road_count = models.FloatField()
    residential_road_count = models.FloatField()

    class Meta:
        abstract = True


class RoadSummaryCountryStats(BaseRoadSummaryStats):

    country = models.ForeignKey(Country, models.DO_NOTHING,
                                 db_column='country_id', blank=True,
                                 null=True)

    class Meta:
        managed = False
        db_table = 'mv_flood_event_road_country_summary'


class RoadSummaryDistrictStats(BaseRoadSummaryStats):

    district = models.ForeignKey(District, models.DO_NOTHING,
                                 db_column='district_id', blank=True,
                                 null=True)

    objects = CountryFilterManager()

    class Meta:
        managed = False
        db_table = 'mv_flood_event_road_district_summary'


class RoadSummarySubDistrictStats(BaseRoadSummaryStats):

    district = models.ForeignKey(District, models.DO_NOTHING,
                                 db_column='district_id', blank=True,
                                 null=True)
    sub_district = models.ForeignKey(SubDistrict, models.DO_NOTHING,
                                     db_column='sub_district_id', blank=True,
                                     null=True)

    class Meta:
        managed = False
        db_table = 'mv_flood_event_road_sub_district_summary'


class BaseCensusPopulationSummaryStats(BaseSummaryStats):

    population_count = models.FloatField()
    impacted_population_count = models.FloatField(db_column='flooded_population_count')

    class Meta:
        abstract = True


class CensusPopulationSummaryCountryStats(BaseCensusPopulationSummaryStats):

    country = models.ForeignKey(Country, models.DO_NOTHING,
                                 db_column='country_id', blank=True,
                                 null=True)

    class Meta:
        managed = False
        db_table = 'mv_flood_event_population_country_summary'


class CensusPopulationSummaryDistrictStats(BaseCensusPopulationSummaryStats):

    district = models.ForeignKey(District, models.DO_NOTHING,
                                 db_column='district_id', blank=True,
                                 null=True)

    objects = CountryFilterManager()

    class Meta:
        managed = False
        db_table = 'mv_flood_event_population_district_summary'


class CensusPopulationSummarySubDistrictStats(
        BaseCensusPopulationSummaryStats):

    district = models.ForeignKey(District, models.DO_NOTHING,
                                 db_column='district_id', blank=True,
                                 null=True)
    sub_district = models.ForeignKey(SubDistrict, models.DO_NOTHING,
                                     db_column='sub_district_id', blank=True,
                                     null=True)

    class Meta:
        managed = False
        db_table = 'mv_flood_event_population_sub_district_summary'
