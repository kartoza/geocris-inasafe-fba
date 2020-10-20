from django.contrib.gis.db import models

from fba.models.all import District, SubDistrict
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


class BaseSummaryStats(base_model):

    flood_event = models.ForeignKey(HazardEvent, models.DO_NOTHING,
                                    db_column='flood_event_id', blank=True,
                                    null=True)
    trigger_status = models.ForeignKey('TriggerStatus', models.DO_NOTHING,
                                       db_column='trigger_status', blank=True,
                                       null=True)

    class Meta:
        abstract = True


class BaseBuildingSummaryStats(BaseSummaryStats):

    building_count = models.FloatField()
    flooded_building_count = models.FloatField()
    total_vulnerability_score = models.FloatField()
    # flooded count
    residential_flooded_building_count = models.FloatField()
    clinic_dr_flooded_building_count = models.FloatField()
    fire_station_flooded_building_count = models.FloatField()
    school_flooded_building_count = models.FloatField()
    university_flooded_building_count = models.FloatField()
    government_flooded_building_count = models.FloatField()
    hospital_flooded_building_count = models.FloatField()
    police_station_flooded_building_count = models.FloatField()
    supermarket_flooded_building_count = models.FloatField()
    sports_facility_flooded_building_count = models.FloatField()
    # not flooded count
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


class BuildingSummaryDistrictStats(BaseBuildingSummaryStats):

    district = models.ForeignKey(District, models.DO_NOTHING,
                                 db_column='district_id', blank=True,
                                 null=True)

    class Meta:
        managed = False
        db_table = 'mv_flood_event_district_summary'


class BuildingSummarySubDistrictStats(BaseBuildingSummaryStats):

    sub_district = models.ForeignKey(SubDistrict, models.DO_NOTHING,
                                     db_column='sub_district_id', blank=True,
                                     null=True)

    class Meta:
        managed = False
        db_table = 'mv_flood_event_sub_district_summary'


class BaseCensusPopulationSummaryStats(BaseSummaryStats):

    population_count = models.FloatField()
    flooded_population_count = models.FloatField()

    class Meta:
        abstract = True


class CensusPopulationSummaryDistrictStats(BaseCensusPopulationSummaryStats):

    district = models.ForeignKey(District, models.DO_NOTHING,
                                 db_column='district_id', blank=True,
                                 null=True)

    class Meta:
        managed = False
        db_table = 'mv_flood_event_population_district_summary'


class CensusPopulationSummarySubDistrictStats(
        BaseCensusPopulationSummaryStats):

    sub_district = models.ForeignKey(SubDistrict, models.DO_NOTHING,
                                     db_column='sub_district_id', blank=True,
                                     null=True)

    class Meta:
        managed = False
        db_table = 'mv_flood_event_population_sub_district_summary'
