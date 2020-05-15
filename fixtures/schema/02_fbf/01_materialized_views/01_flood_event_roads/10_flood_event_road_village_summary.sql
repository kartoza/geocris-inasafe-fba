--
-- Name: mv_hazard_event_road_village_summary; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--
DROP MATERIALIZED VIEW IF EXISTS public.mv_hazard_event_road_village_summary;
CREATE MATERIALIZED VIEW public.mv_hazard_event_road_village_summary AS
 WITH non_hazarded_count_selection AS (
         SELECT b_1.district_id,
            b_1.sub_district_id,
            b_1.village_id,
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
           FROM ( SELECT DISTINCT mv_roads_summary.district_id,
                    mv_roads_summary.sub_district_id,
                    mv_roads_summary.village_id,
                    mv_roads_summary.road_type_count,
                        CASE
                            WHEN ((mv_roads_summary.road_type)::text = 'Motorway or highway'::text) THEN mv_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS motorway_highway_road_count,
                        CASE
                            WHEN ((mv_roads_summary.road_type)::text = 'Tertiary link'::text) THEN mv_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS tertiary_link_road_count,
                        CASE
                            WHEN ((mv_roads_summary.road_type)::text = 'Secondary'::text) THEN mv_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS secondary_road_count,
                        CASE
                            WHEN ((mv_roads_summary.road_type)::text = 'Secondary link'::text) THEN mv_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS secondary_link_road_count,
                        CASE
                            WHEN ((mv_roads_summary.road_type)::text = 'Tertiary'::text) THEN mv_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS tertiary_road_count,
                        CASE
                            WHEN ((mv_roads_summary.road_type)::text = 'Primary link'::text) THEN mv_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS primary_link_road_count,
                        CASE
                            WHEN ((mv_roads_summary.road_type)::text = 'Track'::text) THEN mv_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS track_road_count,
                        CASE
                            WHEN ((mv_roads_summary.road_type)::text = 'Primary road'::text) THEN mv_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS primary_road_count,
                        CASE
                            WHEN ((mv_roads_summary.road_type)::text = 'Motorway link'::text) THEN mv_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS motorway_link_road_count,
                        CASE
                            WHEN ((mv_roads_summary.road_type)::text = 'Road, residential, living street, etc.'::text) THEN mv_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS residential_road_count
                   FROM public.mv_roads_summary
                  WHERE ((mv_roads_summary.district_id IS NOT NULL) AND (mv_roads_summary.sub_district_id IS NOT NULL) AND (mv_roads_summary.village_id IS NOT NULL))) b_1
          GROUP BY b_1.district_id, b_1.sub_district_id, b_1.village_id
        ), hazarded_count_selection AS (
         SELECT a.hazard_event_id,
            a.district_id,
            a.sub_district_id,
            a.village_id,
            sum(a.road_type_count) AS hazarded_road_count,
            sum(a.motorway_highway_road_count) AS motorway_highway_hazarded_road_count,
            sum(a.tertiary_link_road_count) AS tertiary_link_hazarded_road_count,
            sum(a.secondary_road_count) AS secondary_hazarded_road_count,
            sum(a.secondary_link_road_count) AS secondary_link_hazarded_road_count,
            sum(a.tertiary_road_count) AS tertiary_hazarded_road_count,
            sum(a.primary_link_road_count) AS primary_link_hazarded_road_count,
            sum(a.track_road_count) AS track_hazarded_road_count,
            sum(a.primary_road_count) AS primary_hazarded_road_count,
            sum(a.motorway_link_road_count) AS motorway_link_hazarded_road_count,
            sum(a.residential_road_count) AS residential_hazarded_road_count,
            sum(a.total_vulnerability_score) AS total_vulnerability_score
           FROM ( SELECT DISTINCT mv_hazarded_roads_summary.hazard_event_id,
                    mv_hazarded_roads_summary.district_id,
                    mv_hazarded_roads_summary.sub_district_id,
                    mv_hazarded_roads_summary.village_id,
                    mv_hazarded_roads_summary.road_type_count,
                        CASE
                            WHEN ((mv_hazarded_roads_summary.road_type)::text = 'Motorway or highway'::text) THEN mv_hazarded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS motorway_highway_road_count,
                        CASE
                            WHEN ((mv_hazarded_roads_summary.road_type)::text = 'Tertiary link'::text) THEN mv_hazarded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS tertiary_link_road_count,
                        CASE
                            WHEN ((mv_hazarded_roads_summary.road_type)::text = 'Secondary'::text) THEN mv_hazarded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS secondary_road_count,
                        CASE
                            WHEN ((mv_hazarded_roads_summary.road_type)::text = 'Secondary link'::text) THEN mv_hazarded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS secondary_link_road_count,
                        CASE
                            WHEN ((mv_hazarded_roads_summary.road_type)::text = 'Tertiary'::text) THEN mv_hazarded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS tertiary_road_count,
                        CASE
                            WHEN ((mv_hazarded_roads_summary.road_type)::text = 'Primary link'::text) THEN mv_hazarded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS primary_link_road_count,
                        CASE
                            WHEN ((mv_hazarded_roads_summary.road_type)::text = 'Track'::text) THEN mv_hazarded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS track_road_count,
                        CASE
                            WHEN ((mv_hazarded_roads_summary.road_type)::text = 'Primary road'::text) THEN mv_hazarded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS primary_road_count,
                        CASE
                            WHEN ((mv_hazarded_roads_summary.road_type)::text = 'Motorway link'::text) THEN mv_hazarded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS motorway_link_road_count,
                        CASE
                            WHEN ((mv_hazarded_roads_summary.road_type)::text = 'Road, residential, living street, etc.'::text) THEN mv_hazarded_roads_summary.road_type_count
                            ELSE (0)::bigint
                        END AS residential_road_count,
                    mv_hazarded_roads_summary.total_vulnerability_score
                   FROM public.mv_hazarded_roads_summary
                  WHERE ((mv_hazarded_roads_summary.district_id IS NOT NULL) AND (mv_hazarded_roads_summary.sub_district_id IS NOT NULL) AND (mv_hazarded_roads_summary.village_id IS NOT NULL))) a
          GROUP BY a.district_id, a.sub_district_id, a.village_id, a.hazard_event_id
        ), hazarded_aggregate_count AS (
         SELECT a.hazard_event_id,
            a.district_id,
            a.sub_district_id,
            a.village_id,
            a.hazarded_road_count,
            a.motorway_highway_hazarded_road_count,
            a.tertiary_link_hazarded_road_count,
            a.secondary_hazarded_road_count,
            a.secondary_link_hazarded_road_count,
            a.tertiary_hazarded_road_count,
            a.primary_link_hazarded_road_count,
            a.track_hazarded_road_count,
            a.primary_hazarded_road_count,
            a.motorway_link_hazarded_road_count,
            a.residential_hazarded_road_count,
            a.total_vulnerability_score,
            village.name,
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
            b_1.residential_road_count
           FROM ((hazarded_count_selection a
                 JOIN non_hazarded_count_selection b_1 ON ((
                         (a.district_id = b_1.district_id) AND
                         (a.sub_district_id = b_1.sub_district_id) AND
                         (a.village_id = b_1.village_id))))
                      JOIN village ON ((village.village_code = a.village_id)))
        )
 SELECT hazarded_aggregate_count.hazard_event_id,
    hazarded_aggregate_count.district_id,
    hazarded_aggregate_count.sub_district_id,
    hazarded_aggregate_count.village_id,
    hazarded_aggregate_count.hazarded_road_count,
    hazarded_aggregate_count.motorway_highway_hazarded_road_count,
    hazarded_aggregate_count.tertiary_link_hazarded_road_count,
    hazarded_aggregate_count.secondary_hazarded_road_count,
    hazarded_aggregate_count.secondary_link_hazarded_road_count,
    hazarded_aggregate_count.tertiary_hazarded_road_count,
    hazarded_aggregate_count.primary_link_hazarded_road_count,
    hazarded_aggregate_count.track_hazarded_road_count,
    hazarded_aggregate_count.primary_hazarded_road_count,
    hazarded_aggregate_count.motorway_link_hazarded_road_count,
    hazarded_aggregate_count.residential_hazarded_road_count,
    hazarded_aggregate_count.total_vulnerability_score,
    hazarded_aggregate_count.name,
    hazarded_aggregate_count.road_count,
    hazarded_aggregate_count.motorway_highway_road_count,
    hazarded_aggregate_count.tertiary_link_road_count,
    hazarded_aggregate_count.secondary_road_count,
    hazarded_aggregate_count.secondary_link_road_count,
    hazarded_aggregate_count.tertiary_road_count,
    hazarded_aggregate_count.primary_link_road_count,
    hazarded_aggregate_count.track_road_count,
    hazarded_aggregate_count.primary_road_count,
    hazarded_aggregate_count.motorway_link_road_count,
    hazarded_aggregate_count.residential_road_count,
    b.trigger_status
   FROM (hazarded_aggregate_count
     LEFT JOIN village_trigger_status b ON (((b.village_id =
                                                      hazarded_aggregate_count.village_id) AND
                                                     (hazarded_aggregate_count.hazard_event_id =
                                                      b.hazard_event_id))))
    WITH NO DATA;
