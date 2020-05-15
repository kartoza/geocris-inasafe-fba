--
-- Name: mv_roads_summary; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--
DROP MATERIALIZED VIEW IF EXISTS public.mv_roads_summary;
CREATE MATERIALIZED VIEW public.mv_roads_summary AS
 SELECT DISTINCT osm_roads.district_id,
    osm_roads.sub_district_id,
    osm_roads.village_id,
    osm_roads.road_type,
    count(*) OVER (PARTITION BY osm_roads.district_id) AS district_count,
    count(*) OVER (PARTITION BY osm_roads.sub_district_id) AS sub_district_count,
    count(*) OVER (PARTITION BY osm_roads.village_id) AS village_count,
    count(*) OVER (PARTITION BY osm_roads.village_id, osm_roads.road_type) AS road_type_count
   FROM public.osm_roads
  ORDER BY osm_roads.district_id, osm_roads.sub_district_id, osm_roads.village_id, osm_roads.road_type
  WITH NO DATA;
