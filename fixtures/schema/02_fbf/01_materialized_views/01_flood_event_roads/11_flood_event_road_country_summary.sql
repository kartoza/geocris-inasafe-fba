--
-- Name: flood_event_road_country_summary.sql; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--
DROP MATERIALIZED VIEW IF EXISTS public.mv_flood_event_road_country_summary;
CREATE MATERIALIZED VIEW public.mv_flood_event_road_country_summary AS
WITH flooded_aggregate_count AS (
    SELECT c.country_code as country_id,
           c.name         as country_name,
           a.*
    FROM mv_flood_event_road_district_summary a
             JOIN district d on a.district_id = d.dc_code
             JOIN country c on d.country_code = c.country_code
)
SELECT row_number() over ()                   as id,
       flooded_aggregate_count.flood_event_id,
       flooded_aggregate_count.country_id,
       flooded_aggregate_count.country_name   as name,
       sum(flooded_aggregate_count.road_count) as road_count,
       sum(flooded_aggregate_count.motorway_highway_road_count) as motorway_highway_road_count,
       sum(flooded_aggregate_count.tertiary_link_road_count) as tertiary_link_road_count,
       sum(flooded_aggregate_count.secondary_road_count) as secondary_road_count,
       sum(flooded_aggregate_count.secondary_link_road_count) as secondary_link_road_count,
       sum(flooded_aggregate_count.tertiary_road_count) as tertiary_road_count,
       sum(flooded_aggregate_count.primary_link_road_count) as primary_link_road_count,
       sum(flooded_aggregate_count.track_road_count) as track_road_count,
       sum(flooded_aggregate_count.primary_road_count) as primary_road_count,
       sum(flooded_aggregate_count.motorway_link_road_count) as motorway_link_road_count,
       sum(flooded_aggregate_count.residential_road_count) as residential_road_count,
       sum(flooded_aggregate_count.flooded_road_count) as flooded_road_count,
       sum(flooded_aggregate_count.motorway_highway_flooded_road_count) as motorway_highway_flooded_road_count,
       sum(flooded_aggregate_count.tertiary_link_flooded_road_count) as tertiary_link_flooded_road_count,
       sum(flooded_aggregate_count.secondary_flooded_road_count) as secondary_flooded_road_count,
       sum(flooded_aggregate_count.secondary_link_flooded_road_count) as secondary_link_flooded_road_count,
       sum(flooded_aggregate_count.tertiary_flooded_road_count) as tertiary_flooded_road_count,
       sum(flooded_aggregate_count.primary_link_flooded_road_count) as primary_link_flooded_road_count,
       sum(flooded_aggregate_count.track_flooded_road_count) as track_flooded_road_count,
       sum(flooded_aggregate_count.primary_flooded_road_count) as primary_flooded_road_count,
       sum(flooded_aggregate_count.motorway_link_flooded_road_count) as motorway_link_flooded_road_count,
       sum(flooded_aggregate_count.residential_flooded_road_count) as residential_flooded_road_count,
       sum(flooded_aggregate_count.total_vulnerability_score) as total_vulnerability_score,
       max(flooded_aggregate_count.trigger_status) as trigger_status
FROM flooded_aggregate_count
   GROUP BY flood_event_id, country_id, country_name
WITH NO DATA;

CREATE UNIQUE INDEX IF NOT EXISTS mv_flood_event_road_country_summary_idx ON
    mv_flood_event_road_country_summary (id)
