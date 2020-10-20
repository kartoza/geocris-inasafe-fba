# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create,
#   modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field
# names.
from django.contrib.gis.db import models

from fba.models.base import base_model
from fba.models.hazard_event import HazardEvent


class BuildingTypeClass(base_model):
    id = models.AutoField(primary_key=True)
    building_class = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'building_type_class'

    def __str__(self):
        return '{}'.format(self.building_class)


class Census(base_model):
    id = models.BigAutoField(primary_key=True)
    population = models.BigIntegerField(blank=True, null=True)
    elderly = models.BigIntegerField(blank=True, null=True)
    females = models.BigIntegerField(blank=True, null=True)
    males = models.BigIntegerField(blank=True, null=True)
    unemployed = models.BigIntegerField(blank=True, null=True)
    village = models.ForeignKey('Village', models.DO_NOTHING, unique=True,
                                blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'census'


class CensusKemendagri(base_model):
    objectid = models.BigIntegerField(unique=True)
    no_prop = models.FloatField(blank=True, null=True)
    no_kab = models.FloatField(blank=True, null=True)
    no_kec = models.FloatField(blank=True, null=True)
    no_kel = models.FloatField(blank=True, null=True)
    kode_desa_field = models.CharField(db_column='kode_desa_', max_length=25,
                                       blank=True,
                                       null=True)  # Field renamed because
    # it ended with '_'.
    nama_prop_field = models.CharField(db_column='nama_prop_', max_length=40,
                                       blank=True,
                                       null=True)  # Field renamed because
    # it ended with '_'.
    nama_kab_s = models.CharField(primary_key=True, max_length=40)
    nama_kec_s = models.CharField(max_length=40)
    nama_kel_s = models.CharField(max_length=40)
    jumlah_pen = models.FloatField(blank=True, null=True)
    jumlah_kk = models.FloatField(blank=True, null=True)
    pria = models.FloatField(blank=True, null=True)
    wanita = models.FloatField(blank=True, null=True)
    u0 = models.FloatField(blank=True, null=True)
    u5 = models.FloatField(blank=True, null=True)
    u10 = models.FloatField(blank=True, null=True)
    u15 = models.FloatField(blank=True, null=True)
    u20 = models.FloatField(blank=True, null=True)
    u25 = models.FloatField(blank=True, null=True)
    u30 = models.FloatField(blank=True, null=True)
    u35 = models.FloatField(blank=True, null=True)
    u40 = models.FloatField(blank=True, null=True)
    u45 = models.FloatField(blank=True, null=True)
    u50 = models.FloatField(blank=True, null=True)
    u55 = models.FloatField(blank=True, null=True)
    u60 = models.FloatField(blank=True, null=True)
    u65 = models.FloatField(blank=True, null=True)
    u70 = models.FloatField(blank=True, null=True)
    u75 = models.FloatField(blank=True, null=True)
    p01_belum_field = models.FloatField(db_column='p01_belum_', blank=True,
                                        null=True)  # Field renamed because
    # it ended with '_'.

    class Meta:
        managed = False
        db_table = 'census_kemendagri'
        unique_together = (('nama_kab_s', 'nama_kec_s', 'nama_kel_s'),)


class Config(base_model):
    key = models.CharField(unique=True, max_length=255, blank=True, null=True)
    value = models.TextField(blank=True,
                             null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'config'


class AdminBoundaryGlobalKeyMapping(base_model):
    id = models.BigAutoField(primary_key=True)
    id_mapping = models.BigIntegerField()
    key = models.CharField(max_length=255)
    partition = models.CharField(max_length=255)
    partition_level = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'admin_boundary_global_key_mapping'


class Country(base_model):
    id = models.IntegerField()
    geom = models.MultiPolygonField(blank=True, null=True)
    country_code = models.FloatField(primary_key=True)
    name = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'country'


class District(base_model):
    id = models.IntegerField()
    geom = models.MultiPolygonField(blank=True, null=True)
    country = models.ForeignKey(Country, models.DO_NOTHING,
                                db_column='country_code', blank=True,
                                null=True)
    prov_code = models.FloatField(blank=True, null=True)
    dc_code = models.FloatField(primary_key=True)
    name = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'district'


class DistrictTriggerStatus(base_model):
    id = models.AutoField(primary_key=True)
    district_id = models.FloatField(blank=True, null=True)
    trigger_status = models.ForeignKey('TriggerStatus', models.DO_NOTHING,
                                       db_column='trigger_status', blank=True,
                                       null=True)
    flood_event_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'district_trigger_status'


class Hazard(base_model):
    geometry = models.MultiPolygonField(blank=True, null=True)
    name = models.CharField(max_length=80, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    reporting_date_time = models.DateTimeField(blank=True, null=True)
    forecast_date_time = models.DateTimeField(blank=True, null=True)
    station = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hazard'


class HazardArea(base_model):
    depth_class = models.ForeignKey('HazardClass', models.DO_NOTHING,
                                    db_column='depth_class', blank=True,
                                    null=True)
    geometry = models.MultiPolygonField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hazard_area'


class HazardAreas(base_model):
    flood_map = models.ForeignKey('HazardMap', models.DO_NOTHING, blank=True,
                                  null=True)
    flooded_area = models.ForeignKey(HazardArea, models.DO_NOTHING,
                                     blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hazard_areas'


class HazardClass(base_model):
    id = models.AutoField(primary_key=True)
    min_m = models.FloatField(blank=True, null=True)
    max_m = models.FloatField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    hazard_type = models.ForeignKey('HazardType', models.DO_NOTHING,
                                    db_column='hazard_type', blank=True,
                                    null=True)

    class Meta:
        managed = False
        db_table = 'hazard_class'

    def __str__(self):
        return self.label


class HazardMap(base_model):
    notes = models.CharField(max_length=255, blank=True, null=True)
    measuring_station = models.ForeignKey('ReportingPoint', models.DO_NOTHING,
                                          blank=True, null=True)
    place_name = models.CharField(max_length=255, blank=True, null=True)
    return_period = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hazard_map'

    def __str__(self):
        return self.place_name


class HazardType(base_model):
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hazard_type'

    def __str__(self):
        return self.name


class LayerStyles(base_model):
    f_table_catalog = models.CharField(max_length=255, blank=True, null=True)
    f_table_schema = models.CharField(max_length=255, blank=True, null=True)
    f_table_name = models.CharField(max_length=255, blank=True, null=True)
    f_geometry_column = models.CharField(max_length=255, blank=True,
                                         null=True)
    stylename = models.CharField(max_length=30, blank=True, null=True)
    styleqml = models.TextField(blank=True,
                                null=True)  # This field type is a guess.
    stylesld = models.TextField(blank=True,
                                null=True)  # This field type is a guess.
    useasdefault = models.BooleanField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    owner = models.CharField(max_length=30, blank=True, null=True)
    ui = models.TextField(blank=True,
                          null=True)  # This field type is a guess.
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'layer_styles'


class OsmAdmin(base_model):
    id = models.AutoField(primary_key=True)
    osm_id = models.BigIntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    admin_level = models.IntegerField(blank=True, null=True)
    geometry = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'osm_admin'
        unique_together = (('osm_id', 'id'),)


class OsmBuildings(base_model):
    id = models.AutoField(primary_key=True)
    osm_id = models.BigIntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)
    leisure = models.CharField(max_length=255, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    building_levels = models.CharField(db_column='building:levels',
                                       max_length=255, blank=True,
                                       null=True)  # Field renamed to
    # remove unsuitable characters.
    building_height = models.IntegerField(db_column='building:height',
                                          blank=True,
                                          null=True)  # Field renamed to
    # remove unsuitable characters.
    building_min_level = models.IntegerField(db_column='building:min_level',
                                             blank=True,
                                             null=True)  # Field renamed to
    # remove unsuitable characters.
    roof_height = models.IntegerField(db_column='roof:height', blank=True,
                                      null=True)  # Field renamed to remove
    # unsuitable characters.
    roof_material = models.CharField(db_column='roof:material',
                                     max_length=255, blank=True,
                                     null=True)  # Field renamed to remove
    # unsuitable characters.
    building_material = models.CharField(db_column='building:material',
                                         max_length=255, blank=True,
                                         null=True)  # Field renamed to
    # remove unsuitable characters.
    use = models.CharField(max_length=255, blank=True, null=True)
    religion = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    amenity = models.CharField(max_length=255, blank=True, null=True)
    landuse = models.CharField(max_length=255, blank=True, null=True)
    geometry = models.GeometryField(blank=True, null=True)
    building_type = models.CharField(max_length=100, blank=True, null=True)
    building_type_score = models.FloatField(blank=True, null=True)
    building_area = models.FloatField(blank=True, null=True)
    building_area_score = models.FloatField(blank=True, null=True)
    building_material_score = models.FloatField(blank=True, null=True)
    building_road_length = models.FloatField(blank=True, null=True)
    building_road_density_score = models.FloatField(blank=True, null=True)
    total_vulnerability = models.FloatField(blank=True, null=True)
    village = models.ForeignKey('Village', models.DO_NOTHING, blank=True,
                                null=True)
    sub_district = models.ForeignKey('SubDistrict', models.DO_NOTHING,
                                     blank=True, null=True)
    district = models.ForeignKey(District, models.DO_NOTHING, blank=True,
                                 null=True)
    building_road_density = models.IntegerField(blank=True, null=True)
    building_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'osm_buildings'
        unique_together = (('osm_id', 'id'),)


class OsmRoads(base_model):
    id = models.AutoField(primary_key=True)
    osm_id = models.BigIntegerField()
    type = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    oneway = models.SmallIntegerField(blank=True, null=True)
    z_order = models.IntegerField(blank=True, null=True)
    service = models.CharField(max_length=255, blank=True, null=True)
    class_field = models.CharField(db_column='class', max_length=255,
                                   blank=True,
                                   null=True)  # Field renamed because it
    # was a Python reserved word.
    geometry = models.LineStringField(blank=True, null=True)
    road_type = models.CharField(max_length=50, blank=True, null=True)
    road_type_score = models.DecimalField(max_digits=65535,
                                          decimal_places=65535, blank=True,
                                          null=True)
    road_id = models.IntegerField(blank=True, null=True)
    village = models.ForeignKey('Village', models.DO_NOTHING, blank=True,
                                null=True)
    sub_district = models.ForeignKey('SubDistrict', models.DO_NOTHING,
                                     blank=True, null=True)
    district = models.ForeignKey(District, models.DO_NOTHING, blank=True,
                                 null=True)

    class Meta:
        managed = False
        db_table = 'osm_roads'
        unique_together = (('osm_id', 'id'),)


class OsmWaterways(base_model):
    id = models.AutoField(primary_key=True)
    osm_id = models.BigIntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)
    waterway = models.CharField(max_length=255, blank=True, null=True)
    geometry = models.LineStringField(blank=True, null=True)
    waterway_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'osm_waterways'
        unique_together = (('osm_id', 'id'),)


class ProgressStatus(base_model):
    status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'progress_status'


class ReportNotes(base_model):
    notes = models.TextField(blank=True, null=True)
    hazard_type = models.ForeignKey(HazardType, models.DO_NOTHING,
                                    db_column='hazard_type', blank=True,
                                    null=True)
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report_notes'


class ReportingPoint(base_model):
    id = models.BigAutoField(primary_key=True)
    glofas_id = models.BigIntegerField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=80, blank=True, null=True)
    geometry = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reporting_point'

    def __str__(self):
        return self.name


class RoadTypeClass(base_model):
    road_class = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'road_type_class'


class SpreadsheetReports(base_model):
    flood_event = models.ForeignKey(HazardEvent, models.DO_NOTHING,
                                    blank=True, null=True)
    spreadsheet = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spreadsheet_reports'


class SubDistrict(base_model):
    id = models.IntegerField()
    geom = models.MultiPolygonField(blank=True, null=True)
    prov_code = models.SmallIntegerField(blank=True, null=True)
    district = models.ForeignKey(District, models.DO_NOTHING,
                                 db_column='dc_code', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    sub_dc_code = models.FloatField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'sub_district'


class SubDistrictTriggerStatus(base_model):
    sub_district_id = models.FloatField(blank=True, null=True)
    trigger_status = models.ForeignKey('TriggerStatus', models.DO_NOTHING,
                                       db_column='trigger_status', blank=True,
                                       null=True)
    flood_event_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sub_district_trigger_status'


class Topology(base_model):
    name = models.CharField(unique=True, max_length=255)
    srid = models.IntegerField()
    precision = models.FloatField()
    hasz = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'topology'


class TriggerStatus(base_model):
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'trigger_status'


class Village(base_model):
    id = models.IntegerField()
    geom = models.MultiPolygonField(blank=True, null=True)
    prov_code = models.FloatField(blank=True, null=True)
    dc_code = models.FloatField(blank=True, null=True)
    sub_dc_code = models.FloatField(blank=True, null=True)
    village_code = models.FloatField(primary_key=True)
    name = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'village'


class VillageTriggerStatus(base_model):
    village_id = models.FloatField(blank=True, null=True)
    trigger_status = models.ForeignKey(TriggerStatus, models.DO_NOTHING,
                                       db_column='trigger_status', blank=True,
                                       null=True)
    flood_event_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'village_trigger_status'


class WaterwayTypeClass(base_model):
    waterway_class = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'waterway_type_class'


class WorldPop(base_model):
    rid = models.AutoField(primary_key=True)
    rast = models.TextField(blank=True,
                            null=True)  # This field type is a guess.
    filename = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'world_pop'

    def __str__(self):
        return '{rid} - {filename}'.format(
            rid=self.rid,
            filename=self.filename
        )


class WorldPopDistrictStats(base_model):
    prov_code = models.FloatField(blank=True, null=True)
    dc_code = models.FloatField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    pop_count = models.FloatField(blank=True, null=True)
    pop_sum = models.FloatField(blank=True, null=True)
    pop_mean = models.FloatField(blank=True, null=True)
    pop_median = models.FloatField(blank=True, null=True)
    pop_min = models.FloatField(blank=True, null=True)
    pop_max = models.FloatField(blank=True, null=True)
    pop_minority = models.FloatField(blank=True, null=True)
    pop_majority = models.FloatField(blank=True, null=True)
    pop_variety = models.IntegerField(blank=True, null=True)
    pop_variance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'world_pop_district_stats'


class WorldPopSubDistrictStats(base_model):
    prov_code = models.SmallIntegerField(blank=True, null=True)
    dc_code = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    sub_dc_code = models.DecimalField(unique=True, max_digits=65535,
                                      decimal_places=65535, blank=True,
                                      null=True)
    pop_count = models.FloatField(blank=True, null=True)
    pop_sum = models.FloatField(blank=True, null=True)
    pop_mean = models.FloatField(blank=True, null=True)
    pop_median = models.FloatField(blank=True, null=True)
    pop_min = models.FloatField(blank=True, null=True)
    pop_max = models.FloatField(blank=True, null=True)
    pop_range = models.FloatField(blank=True, null=True)
    pop_minority = models.FloatField(blank=True, null=True)
    pop_majority = models.FloatField(blank=True, null=True)
    pop_variance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'world_pop_sub_district_stats'


class WorldPopVillageStats(base_model):
    prov_code = models.FloatField(blank=True, null=True)
    dc_code = models.FloatField(blank=True, null=True)
    sub_dc_code = models.FloatField(blank=True, null=True)
    village_code = models.FloatField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    pop_count = models.FloatField(blank=True, null=True)
    pop_sum = models.FloatField(blank=True, null=True)
    pop_mean = models.FloatField(blank=True, null=True)
    pop_median = models.FloatField(blank=True, null=True)
    pop_min = models.FloatField(blank=True, null=True)
    pop_max = models.FloatField(blank=True, null=True)
    pop_minority = models.FloatField(blank=True, null=True)
    pop_majority = models.FloatField(blank=True, null=True)
    pop_variety = models.IntegerField(blank=True, null=True)
    pop_variance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'world_pop_village_stats'
