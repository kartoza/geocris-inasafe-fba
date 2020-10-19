--
-- Name: mv_flood_event_road_district_summary; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--
DROP MATERIALIZED VIEW IF EXISTS public.mv_flood_event_road_district_summary;
CREATE MATERIALIZED VIEW public.mv_flood_event_road_district_summary AS
 WITH non_flooded_count_selection AS (
         SELECT b_1.district_id,
            sum(b_1.road_type_count) AS road_count,
            sum(b_1.motorway_highway_road_count) AS motorway_highway_road_count,
            sum(b_1.tertiary_link_road_count) AS tertiary_link_road_count,
            sum(b_1.secondary_road_count) AS secondary_road_count,
            sum(b_1.secondary_link_road_count) AS secondary_link_road_count,
            sum(b_1.tertiary_road_count) AS tertiary_road_count,
            sum(b_1.primary_link_road_count) AS primary_link_road_count,
            sum(b_1.track_road_count) AS track_road_count,
            sum(b_1.primary_road_count) AS primary_road_count,
            sum(b_1.motorway_link_road_count) AS motorway_link_road_count,
            sum(b_1.residential_road_count) AS residential_road_count
           FROM ( SELECT DISTINCT mv_non_flooded_roads_summary.district_id,
                    mv_non_flooded_roads_summary.sub_district_id,
                    mv_non_flooded_roads_summary.village_id,
                    mv_non_flooded_roads_summary.road_type_count,
                        CASE
                            WHEN ((mv_non_flooded_roads_summary.road_type)::text = 'Motorway or highway'::text) THEN mv_non_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS motorway_highway_road_count,
                        CASE
                            WHEN ((mv_non_flooded_roads_summary.road_type)::text = 'Tertiary link'::text) THEN mv_non_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS tertiary_link_road_count,
                        CASE
                            WHEN ((mv_non_flooded_roads_summary.road_type)::text = 'Secondary'::text) THEN mv_non_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS secondary_road_count,
                        CASE
                            WHEN ((mv_non_flooded_roads_summary.road_type)::text = 'Secondary link'::text) THEN mv_non_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS secondary_link_road_count,
                        CASE
                            WHEN ((mv_non_flooded_roads_summary.road_type)::text = 'Tertiary'::text) THEN mv_non_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS tertiary_road_count,
                        CASE
                            WHEN ((mv_non_flooded_roads_summary.road_type)::text = 'Primary link'::text) THEN mv_non_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS primary_link_road_count,
                        CASE
                            WHEN ((mv_non_flooded_roads_summary.road_type)::text = 'Track'::text) THEN mv_non_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS track_road_count,
                        CASE
                            WHEN ((mv_non_flooded_roads_summary.road_type)::text = 'Primary road'::text) THEN mv_non_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS primary_road_count,
                        CASE
                            WHEN ((mv_non_flooded_roads_summary.road_type)::text = 'Motorway link'::text) THEN mv_non_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS motorway_link_road_count,
                        CASE
                            WHEN ((mv_non_flooded_roads_summary.road_type)::text = 'Road, residential, living street, etc.'::text) THEN mv_non_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS residential_road_count
                   FROM public.mv_non_flooded_roads_summary
                  WHERE ((mv_non_flooded_roads_summary.district_id IS NOT NULL) AND (mv_non_flooded_roads_summary.sub_district_id IS NOT NULL) AND (mv_non_flooded_roads_summary.village_id IS NOT NULL))) b_1
          GROUP BY b_1.district_id
        ), flooded_count_selection AS (
         SELECT a.flood_event_id,
            a.district_id,
            sum(a.road_type_count) AS flooded_road_count,
            sum(a.motorway_highway_road_count) AS motorway_highway_flooded_road_count,
            sum(a.tertiary_link_road_count) AS tertiary_link_flooded_road_count,
            sum(a.secondary_road_count) AS secondary_flooded_road_count,
            sum(a.secondary_link_road_count) AS secondary_link_flooded_road_count,
            sum(a.tertiary_road_count) AS tertiary_flooded_road_count,
            sum(a.primary_link_road_count) AS primary_link_flooded_road_count,
            sum(a.track_road_count) AS track_flooded_road_count,
            sum(a.primary_road_count) AS primary_flooded_road_count,
            sum(a.motorway_link_road_count) AS motorway_link_flooded_road_count,
            sum(a.residential_road_count) AS residential_flooded_road_count,
            sum(a.total_vulnerability_score) AS total_vulnerability_score
           FROM ( SELECT DISTINCT mv_flooded_roads_summary.flood_event_id,
                    mv_flooded_roads_summary.district_id,
                    mv_flooded_roads_summary.sub_district_id,
                    mv_flooded_roads_summary.village_id,
                    mv_flooded_roads_summary.road_type_count,
                        CASE
                            WHEN ((mv_flooded_roads_summary.road_type)::text = 'Motorway or highway'::text) THEN mv_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS motorway_highway_road_count,
                        CASE
                            WHEN ((mv_flooded_roads_summary.road_type)::text = 'Tertiary link'::text) THEN mv_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS tertiary_link_road_count,
                        CASE
                            WHEN ((mv_flooded_roads_summary.road_type)::text = 'Secondary'::text) THEN mv_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS secondary_road_count,
                        CASE
                            WHEN ((mv_flooded_roads_summary.road_type)::text = 'Secondary link'::text) THEN mv_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS secondary_link_road_count,
                        CASE
                            WHEN ((mv_flooded_roads_summary.road_type)::text = 'Tertiary'::text) THEN mv_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS tertiary_road_count,
                        CASE
                            WHEN ((mv_flooded_roads_summary.road_type)::text = 'Primary link'::text) THEN mv_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS primary_link_road_count,
                        CASE
                            WHEN ((mv_flooded_roads_summary.road_type)::text = 'Track'::text) THEN mv_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS track_road_count,
                        CASE
                            WHEN ((mv_flooded_roads_summary.road_type)::text = 'Primary road'::text) THEN mv_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS primary_road_count,
                        CASE
                            WHEN ((mv_flooded_roads_summary.road_type)::text = 'Motorway link'::text) THEN mv_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS motorway_link_road_count,
                        CASE
                            WHEN ((mv_flooded_roads_summary.road_type)::text = 'Road, residential, living street, etc.'::text) THEN mv_flooded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS residential_road_count,
                    mv_flooded_roads_summary.total_vulnerability_score
                   FROM public.mv_flooded_roads_summary
                  WHERE ((mv_flooded_roads_summary.district_id IS NOT NULL) AND (mv_flooded_roads_summary.sub_district_id IS NOT NULL) AND (mv_flooded_roads_summary.village_id IS NOT NULL))) a
          GROUP BY a.district_id, a.flood_event_id
        ), flooded_aggregate_count AS (
         SELECT district.name,
            b_1.road_count,
            b_1.motorway_highway_road_count,
            b_1.tertiary_link_road_count,
            b_1.secondary_road_count,
            b_1.secondary_link_road_count,
            b_1.tertiary_road_count,
            b_1.primary_link_road_count,
            b_1.track_road_count,
            b_1.primary_road_count,
            b_1.motorway_link_road_count,
            b_1.residential_road_count,
            a.flood_event_id,
            a.district_id,
            a.flooded_road_count,
            a.motorway_highway_flooded_road_count,
            a.tertiary_link_flooded_road_count,
            a.secondary_flooded_road_count,
            a.secondary_link_flooded_road_count,
            a.tertiary_flooded_road_count,
            a.primary_link_flooded_road_count,
            a.track_flooded_road_count,
            a.primary_flooded_road_count,
            a.motorway_link_flooded_road_count,
            a.residential_flooded_road_count,
            a.total_vulnerability_score
           FROM ((flooded_count_selection a
             JOIN non_flooded_count_selection b_1 ON ((a.district_id = b_1.district_id)))
             JOIN public.district ON ((district.dc_code = a.district_id)))
        )
 SELECT
    row_number() over () as id,
    flooded_aggregate_count.name,
    flooded_aggregate_count.road_count,
    flooded_aggregate_count.motorway_highway_road_count,
    flooded_aggregate_count.tertiary_link_road_count,
    flooded_aggregate_count.secondary_road_count,
    flooded_aggregate_count.secondary_link_road_count,
    flooded_aggregate_count.tertiary_road_count,
    flooded_aggregate_count.primary_link_road_count,
    flooded_aggregate_count.track_road_count,
    flooded_aggregate_count.primary_road_count,
    flooded_aggregate_count.motorway_link_road_count,
    flooded_aggregate_count.residential_road_count,
    flooded_aggregate_count.flood_event_id,
    flooded_aggregate_count.district_id,
    flooded_aggregate_count.flooded_road_count,
    flooded_aggregate_count.motorway_highway_flooded_road_count,
    flooded_aggregate_count.tertiary_link_flooded_road_count,
    flooded_aggregate_count.secondary_flooded_road_count,
    flooded_aggregate_count.secondary_link_flooded_road_count,
    flooded_aggregate_count.tertiary_flooded_road_count,
    flooded_aggregate_count.primary_link_flooded_road_count,
    flooded_aggregate_count.track_flooded_road_count,
    flooded_aggregate_count.primary_flooded_road_count,
    flooded_aggregate_count.motorway_link_flooded_road_count,
    flooded_aggregate_count.residential_flooded_road_count,
    flooded_aggregate_count.total_vulnerability_score,
    b.trigger_status
   FROM (flooded_aggregate_count
     LEFT JOIN public.district_trigger_status b ON (((b.district_id = flooded_aggregate_count.district_id) AND (flooded_aggregate_count.flood_event_id = b.flood_event_id))))
  WITH NO DATA;

CREATE UNIQUE INDEX IF NOT EXISTS mv_flood_event_road_district_summary ON
    mv_flood_event_road_district_summary(id)
