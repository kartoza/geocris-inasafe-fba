--
-- Name: mv_flood_event_country_summary; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--
DROP MATERIALIZED VIEW IF EXISTS public.mv_flood_event_country_summary;
CREATE MATERIALIZED VIEW public.mv_flood_event_country_summary AS
 WITH flooded_aggregate_count AS (
     SELECT
        c.country_code as country_id,
        c.name as country_name,
        a.*
     FROM mv_flood_event_district_summary a
     JOIN district d on a.district_id = d.dc_code
     JOIN country c on d.country_code = c.country_code
 )
 SELECT
    row_number() over () as id,
    flooded_aggregate_count.flood_event_id as flood_event_id,
    flooded_aggregate_count.country_id,
    flooded_aggregate_count.country_name as name,
    sum(flooded_aggregate_count.building_count) as building_count,
    sum(flooded_aggregate_count.flooded_building_count) as flooded_building_count,
    sum(flooded_aggregate_count.total_vulnerability_score) as total_vulnerability_score,
    sum(flooded_aggregate_count.residential_flooded_building_count) as residential_flooded_building_count,
    sum(flooded_aggregate_count.clinic_dr_flooded_building_count) as clinic_dr_flooded_building_count,
    sum(flooded_aggregate_count.fire_station_flooded_building_count) as fire_station_flooded_building_count,
    sum(flooded_aggregate_count.school_flooded_building_count) as school_flooded_building_count,
    sum(flooded_aggregate_count.university_flooded_building_count) as university_flooded_building_count,
    sum(flooded_aggregate_count.government_flooded_building_count) as government_flooded_building_count,
    sum(flooded_aggregate_count.hospital_flooded_building_count) as hospital_flooded_building_count,
    sum(flooded_aggregate_count.police_station_flooded_building_count) as police_station_flooded_building_count,
    sum(flooded_aggregate_count.supermarket_flooded_building_count) as supermarket_flooded_building_count,
    sum(flooded_aggregate_count.sports_facility_flooded_building_count) as sports_facility_flooded_building_count,
    sum(flooded_aggregate_count.residential_building_count) as residential_building_count,
    sum(flooded_aggregate_count.clinic_dr_building_count) as clinic_dr_building_count,
    sum(flooded_aggregate_count.fire_station_building_count) as fire_station_building_count,
    sum(flooded_aggregate_count.school_building_count) as school_building_count,
    sum(flooded_aggregate_count.university_building_count) as university_building_count,
    sum(flooded_aggregate_count.government_building_count) as government_building_count,
    sum(flooded_aggregate_count.hospital_building_count) as hospital_building_count,
    sum(flooded_aggregate_count.police_station_building_count) as police_station_building_count,
    sum(flooded_aggregate_count.supermarket_building_count) as supermarket_building_count,
    sum(flooded_aggregate_count.sports_facility_building_count) as sports_facility_building_count,
    max(flooded_aggregate_count.trigger_status) as trigger_status
   FROM flooded_aggregate_count
   GROUP BY flood_event_id, country_id, country_name
  WITH NO DATA;

CREATE UNIQUE INDEX IF NOT EXISTS mv_flood_event_country_summary_idx ON
    mv_flood_event_country_summary(id)
