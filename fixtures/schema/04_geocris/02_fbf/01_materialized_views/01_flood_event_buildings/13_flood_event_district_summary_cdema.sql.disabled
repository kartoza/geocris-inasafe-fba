--
-- Name: mv_flood_event_district_summary; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--
DROP MATERIALIZED VIEW IF EXISTS public.mv_flood_event_district_summary;
CREATE MATERIALIZED VIEW public.mv_flood_event_district_summary AS
 WITH non_flooded_count_selection AS (
         SELECT b_1.district_id,
            sum(b_1.building_type_count) AS building_count,
            sum(b_1.residential_building_count) AS residential_building_count,
            sum(b_1.clinic_dr_building_count) AS clinic_dr_building_count,
            sum(b_1.fire_station_building_count) AS fire_station_building_count,
            sum(b_1.school_building_count) AS school_building_count,
            sum(b_1.university_building_count) AS university_building_count,
            sum(b_1.government_building_count) AS government_building_count,
            sum(b_1.hospital_building_count) AS hospital_building_count,
            sum(b_1.police_station_building_count) AS police_station_building_count,
            sum(b_1.supermarket_building_count) AS supermarket_building_count,
            sum(b_1.sports_facility_building_count) AS sports_facility_building_count
           FROM ( SELECT DISTINCT mv_non_flooded_building_summary.district_id,
                    mv_non_flooded_building_summary.sub_district_id,
                    mv_non_flooded_building_summary.village_id,
                    mv_non_flooded_building_summary.building_type_count,
                        CASE
                            WHEN ((mv_non_flooded_building_summary.building_type)::text = 'Residential'::text) THEN mv_non_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS residential_building_count,
                        CASE
                            WHEN ((mv_non_flooded_building_summary.building_type)::text = 'Clinic/Doctor'::text) THEN mv_non_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS clinic_dr_building_count,
                        CASE
                            WHEN ((mv_non_flooded_building_summary.building_type)::text = 'Fire Station'::text) THEN mv_non_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS fire_station_building_count,
                        CASE
                            WHEN ((mv_non_flooded_building_summary.building_type)::text = 'School'::text) THEN mv_non_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS school_building_count,
                        CASE
                            WHEN ((mv_non_flooded_building_summary.building_type)::text = 'University/College'::text) THEN mv_non_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS university_building_count,
                        CASE
                            WHEN ((mv_non_flooded_building_summary.building_type)::text = 'Government'::text) THEN mv_non_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS government_building_count,
                        CASE
                            WHEN ((mv_non_flooded_building_summary.building_type)::text = 'Hospital'::text) THEN mv_non_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS hospital_building_count,
                        CASE
                            WHEN ((mv_non_flooded_building_summary.building_type)::text = 'Police Station'::text) THEN mv_non_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS police_station_building_count,
                        CASE
                            WHEN ((mv_non_flooded_building_summary.building_type)::text = 'Supermarket'::text) THEN mv_non_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS supermarket_building_count,
                        CASE
                            WHEN ((mv_non_flooded_building_summary.building_type)::text = 'Sports Facility'::text) THEN mv_non_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS sports_facility_building_count
                   FROM public.mv_non_flooded_building_summary
                  WHERE (mv_non_flooded_building_summary.district_id IS NOT NULL)) b_1
          GROUP BY b_1.district_id
        ), flooded_count_selection AS (
         SELECT a.flood_event_id,
            a.district_id,
            sum(a.building_type_count) AS flooded_building_count,
            sum(a.residential_building_count) AS residential_flooded_building_count,
            sum(a.clinic_dr_building_count) AS clinic_dr_flooded_building_count,
            sum(a.fire_station_building_count) AS fire_station_flooded_building_count,
            sum(a.school_building_count) AS school_flooded_building_count,
            sum(a.university_building_count) AS university_flooded_building_count,
            sum(a.government_building_count) AS government_flooded_building_count,
            sum(a.hospital_building_count) AS hospital_flooded_building_count,
            sum(a.police_station_building_count) AS police_station_flooded_building_count,
            sum(a.supermarket_building_count) AS supermarket_flooded_building_count,
            sum(a.sports_facility_building_count) AS sports_facility_flooded_building_count,
            sum(a.total_vulnerability_score) AS total_vulnerability_score
           FROM ( SELECT DISTINCT mv_flooded_building_summary.flood_event_id,
                    mv_flooded_building_summary.district_id,
                    mv_flooded_building_summary.sub_district_id,
                    mv_flooded_building_summary.village_id,
                    mv_flooded_building_summary.building_type_count,
                        CASE
                            WHEN ((mv_flooded_building_summary.building_type)::text = 'Residential'::text) THEN mv_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS residential_building_count,
                        CASE
                            WHEN ((mv_flooded_building_summary.building_type)::text = 'Clinic/Doctor'::text) THEN mv_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS clinic_dr_building_count,
                        CASE
                            WHEN ((mv_flooded_building_summary.building_type)::text = 'Fire Station'::text) THEN mv_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS fire_station_building_count,
                        CASE
                            WHEN ((mv_flooded_building_summary.building_type)::text = 'School'::text) THEN mv_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS school_building_count,
                        CASE
                            WHEN ((mv_flooded_building_summary.building_type)::text = 'University/College'::text) THEN mv_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS university_building_count,
                        CASE
                            WHEN ((mv_flooded_building_summary.building_type)::text = 'Government'::text) THEN mv_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS government_building_count,
                        CASE
                            WHEN ((mv_flooded_building_summary.building_type)::text = 'Hospital'::text) THEN mv_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS hospital_building_count,
                        CASE
                            WHEN ((mv_flooded_building_summary.building_type)::text = 'Police Station'::text) THEN mv_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS police_station_building_count,
                        CASE
                            WHEN ((mv_flooded_building_summary.building_type)::text = 'Supermarket'::text) THEN mv_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS supermarket_building_count,
                        CASE
                            WHEN ((mv_flooded_building_summary.building_type)::text = 'Sports Facility'::text) THEN mv_flooded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS sports_facility_building_count,
                    mv_flooded_building_summary.total_vulnerability_score
                   FROM public.mv_flooded_building_summary
                  WHERE (mv_flooded_building_summary.district_id IS NOT NULL)) a
          GROUP BY a.district_id, a.flood_event_id
        ), flooded_aggregate_count AS (
         SELECT a.flood_event_id,
            a.district_id,
            district.name,
            a.flooded_building_count,
            b_1.building_count,
            b_1.residential_building_count,
            b_1.clinic_dr_building_count,
            b_1.fire_station_building_count,
            b_1.school_building_count,
            b_1.university_building_count,
            b_1.government_building_count,
            b_1.hospital_building_count,
            b_1.police_station_building_count,
            b_1.supermarket_building_count,
            b_1.sports_facility_building_count,
            a.residential_flooded_building_count,
            a.clinic_dr_flooded_building_count,
            a.fire_station_flooded_building_count,
            a.school_flooded_building_count,
            a.university_flooded_building_count,
            a.government_flooded_building_count,
            a.hospital_flooded_building_count,
            a.police_station_flooded_building_count,
            a.supermarket_flooded_building_count,
            a.sports_facility_flooded_building_count,
            a.total_vulnerability_score
           FROM ((flooded_count_selection a
             JOIN non_flooded_count_selection b_1 ON ((a.district_id = b_1.district_id)))
             JOIN public.district ON ((district.dc_code = a.district_id)))
        )
 SELECT
    row_number() over () as id,
    flooded_aggregate_count.flood_event_id,
    flooded_aggregate_count.district_id,
    flooded_aggregate_count.name,
    flooded_aggregate_count.building_count,
    flooded_aggregate_count.flooded_building_count,
    flooded_aggregate_count.total_vulnerability_score,
    flooded_aggregate_count.residential_flooded_building_count,
    flooded_aggregate_count.clinic_dr_flooded_building_count,
    flooded_aggregate_count.fire_station_flooded_building_count,
    flooded_aggregate_count.school_flooded_building_count,
    flooded_aggregate_count.university_flooded_building_count,
    flooded_aggregate_count.government_flooded_building_count,
    flooded_aggregate_count.hospital_flooded_building_count,
    flooded_aggregate_count.police_station_flooded_building_count,
    flooded_aggregate_count.supermarket_flooded_building_count,
    flooded_aggregate_count.sports_facility_flooded_building_count,
    flooded_aggregate_count.residential_building_count,
    flooded_aggregate_count.clinic_dr_building_count,
    flooded_aggregate_count.fire_station_building_count,
    flooded_aggregate_count.school_building_count,
    flooded_aggregate_count.university_building_count,
    flooded_aggregate_count.government_building_count,
    flooded_aggregate_count.hospital_building_count,
    flooded_aggregate_count.police_station_building_count,
    flooded_aggregate_count.supermarket_building_count,
    flooded_aggregate_count.sports_facility_building_count,
    b.trigger_status
   FROM (flooded_aggregate_count
     LEFT JOIN public.district_trigger_status b ON (((b.district_id = flooded_aggregate_count.district_id) AND (flooded_aggregate_count.flood_event_id = b.flood_event_id))))
  WITH NO DATA;

CREATE UNIQUE INDEX IF NOT EXISTS mv_flood_event_district_summary ON
    mv_flood_event_district_summary(id)
