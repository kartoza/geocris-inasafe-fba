--
-- Name: mv_building_summary; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--
DROP MATERIALIZED VIEW IF EXISTS public.mv_building_summary;
CREATE MATERIALIZED VIEW public.mv_building_summary AS
 SELECT DISTINCT osm_buildings.district_id,
    osm_buildings.sub_district_id,
    osm_buildings.village_id,
    osm_buildings.building_type,
    count(*) OVER (PARTITION BY osm_buildings.district_id) AS district_count,
    count(*) OVER (PARTITION BY osm_buildings.sub_district_id) AS sub_district_count,
    count(*) OVER (PARTITION BY osm_buildings.village_id) AS village_count,
    count(*) OVER (PARTITION BY osm_buildings.village_id, osm_buildings.building_type) AS building_type_count
   FROM public.osm_buildings
  ORDER BY osm_buildings.district_id, osm_buildings.sub_district_id, osm_buildings.village_id, osm_buildings.building_type
  WITH NO DATA;

