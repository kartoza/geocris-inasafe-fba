--
-- Name: mv_hazard_event_village_summary; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--
DROP MATERIALIZED VIEW IF EXISTS public.mv_hazard_event_village_summary;
CREATE MATERIALIZED VIEW public.mv_hazard_event_village_summary AS
 WITH non_hazarded_count_selection AS (
         SELECT b_1.district_id,
            b_1.sub_district_id,
            b_1.village_id,
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
           FROM ( SELECT DISTINCT mv_building_summary.district_id,
                    mv_building_summary.sub_district_id,
                    mv_building_summary.village_id,
                    mv_building_summary.building_type_count,
                        CASE
                            WHEN ((mv_building_summary.building_type)::text = 'Residential'::text) THEN mv_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS residential_building_count,
                        CASE
                            WHEN ((mv_building_summary.building_type)::text = 'Clinic/Doctor'::text) THEN mv_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS clinic_dr_building_count,
                        CASE
                            WHEN ((mv_building_summary.building_type)::text = 'Fire Station'::text) THEN mv_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS fire_station_building_count,
                        CASE
                            WHEN ((mv_building_summary.building_type)::text = 'School'::text) THEN mv_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS school_building_count,
                        CASE
                            WHEN ((mv_building_summary.building_type)::text = 'University/College'::text) THEN mv_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS university_building_count,
                        CASE
                            WHEN ((mv_building_summary.building_type)::text = 'Government'::text) THEN mv_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS government_building_count,
                        CASE
                            WHEN ((mv_building_summary.building_type)::text = 'Hospital'::text) THEN mv_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS hospital_building_count,
                        CASE
                            WHEN ((mv_building_summary.building_type)::text = 'Police Station'::text) THEN mv_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS police_station_building_count,
                        CASE
                            WHEN ((mv_building_summary.building_type)::text = 'Supermarket'::text) THEN mv_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS supermarket_building_count,
                        CASE
                            WHEN ((mv_building_summary.building_type)::text = 'Sports Facility'::text) THEN mv_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS sports_facility_building_count
                   FROM public.mv_building_summary
                  WHERE ((mv_building_summary.district_id IS NOT NULL) AND (mv_building_summary.sub_district_id IS NOT NULL) AND (mv_building_summary.village_id IS NOT NULL))) b_1
          GROUP BY b_1.district_id, b_1.sub_district_id, b_1.village_id
        ), hazarded_count_selection AS (
         SELECT a.hazard_event_id,
            a.district_id,
            a.sub_district_id,
            a.village_id,
            sum(a.building_type_count) AS hazarded_building_count,
            sum(a.residential_building_count) AS residential_hazarded_building_count,
            sum(a.clinic_dr_building_count) AS clinic_dr_hazarded_building_count,
            sum(a.fire_station_building_count) AS fire_station_hazarded_building_count,
            sum(a.school_building_count) AS school_hazarded_building_count,
            sum(a.university_building_count) AS university_hazarded_building_count,
            sum(a.government_building_count) AS government_hazarded_building_count,
            sum(a.hospital_building_count) AS hospital_hazarded_building_count,
            sum(a.police_station_building_count) AS police_station_hazarded_building_count,
            sum(a.supermarket_building_count) AS supermarket_hazarded_building_count,
            sum(a.sports_facility_building_count) AS sports_facility_hazarded_building_count,
            sum(a.total_vulnerability_score) AS total_vulnerability_score
           FROM ( SELECT DISTINCT mv_hazarded_building_summary.hazard_event_id,
                    mv_hazarded_building_summary.district_id,
                    mv_hazarded_building_summary.sub_district_id,
                    mv_hazarded_building_summary.village_id,
                    mv_hazarded_building_summary.building_type_count,
                        CASE
                            WHEN ((mv_hazarded_building_summary.building_type)::text = 'Residential'::text) THEN mv_hazarded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS residential_building_count,
                        CASE
                            WHEN ((mv_hazarded_building_summary.building_type)::text = 'Clinic/Doctor'::text) THEN mv_hazarded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS clinic_dr_building_count,
                        CASE
                            WHEN ((mv_hazarded_building_summary.building_type)::text = 'Fire Station'::text) THEN mv_hazarded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS fire_station_building_count,
                        CASE
                            WHEN ((mv_hazarded_building_summary.building_type)::text = 'School'::text) THEN mv_hazarded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS school_building_count,
                        CASE
                            WHEN ((mv_hazarded_building_summary.building_type)::text = 'University/College'::text) THEN mv_hazarded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS university_building_count,
                        CASE
                            WHEN ((mv_hazarded_building_summary.building_type)::text = 'Government'::text) THEN mv_hazarded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS government_building_count,
                        CASE
                            WHEN ((mv_hazarded_building_summary.building_type)::text = 'Hospital'::text) THEN mv_hazarded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS hospital_building_count,
                        CASE
                            WHEN ((mv_hazarded_building_summary.building_type)::text = 'Police Station'::text) THEN mv_hazarded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS police_station_building_count,
                        CASE
                            WHEN ((mv_hazarded_building_summary.building_type)::text = 'Supermarket'::text) THEN mv_hazarded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS supermarket_building_count,
                        CASE
                            WHEN ((mv_hazarded_building_summary.building_type)::text = 'Sports Facility'::text) THEN mv_hazarded_building_summary.building_type_count
                            ELSE (0)::bigint
                        END AS sports_facility_building_count,
                    mv_hazarded_building_summary.total_vulnerability_score
                   FROM public.mv_hazarded_building_summary
                  WHERE ((mv_hazarded_building_summary.district_id IS NOT NULL) AND (mv_hazarded_building_summary.sub_district_id IS NOT NULL) AND (mv_hazarded_building_summary.village_id IS NOT NULL))) a
          GROUP BY a.district_id, a.sub_district_id, a.village_id, a.hazard_event_id
        ), hazarded_aggregate_count AS (
         SELECT a.hazard_event_id,
            a.district_id,
            a.sub_district_id,
            a.village_id,
            village.name,
            a.hazarded_building_count,
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
            a.residential_hazarded_building_count,
            a.clinic_dr_hazarded_building_count,
            a.fire_station_hazarded_building_count,
            a.school_hazarded_building_count,
            a.university_hazarded_building_count,
            a.government_hazarded_building_count,
            a.hospital_hazarded_building_count,
            a.police_station_hazarded_building_count,
            a.supermarket_hazarded_building_count,
            a.sports_facility_hazarded_building_count,
            a.total_vulnerability_score
           FROM ((hazarded_count_selection a
             JOIN non_hazarded_count_selection b_1 ON (((a.district_id = b_1.district_id) AND (a.sub_district_id = b_1.sub_district_id) AND (a.village_id = b_1.village_id))))
             JOIN public.village ON ((village.village_code = a.village_id)))
        )
 SELECT hazarded_aggregate_count.hazard_event_id,
    hazarded_aggregate_count.district_id,
    hazarded_aggregate_count.sub_district_id,
    hazarded_aggregate_count.village_id,
    hazarded_aggregate_count.name,
    hazarded_aggregate_count.building_count,
    hazarded_aggregate_count.hazarded_building_count,
    hazarded_aggregate_count.total_vulnerability_score,
    hazarded_aggregate_count.residential_hazarded_building_count,
    hazarded_aggregate_count.clinic_dr_hazarded_building_count,
    hazarded_aggregate_count.fire_station_hazarded_building_count,
    hazarded_aggregate_count.school_hazarded_building_count,
    hazarded_aggregate_count.university_hazarded_building_count,
    hazarded_aggregate_count.government_hazarded_building_count,
    hazarded_aggregate_count.hospital_hazarded_building_count,
    hazarded_aggregate_count.police_station_hazarded_building_count,
    hazarded_aggregate_count.supermarket_hazarded_building_count,
    hazarded_aggregate_count.sports_facility_hazarded_building_count,
    hazarded_aggregate_count.residential_building_count,
    hazarded_aggregate_count.clinic_dr_building_count,
    hazarded_aggregate_count.fire_station_building_count,
    hazarded_aggregate_count.school_building_count,
    hazarded_aggregate_count.university_building_count,
    hazarded_aggregate_count.government_building_count,
    hazarded_aggregate_count.hospital_building_count,
    hazarded_aggregate_count.police_station_building_count,
    hazarded_aggregate_count.supermarket_building_count,
    hazarded_aggregate_count.sports_facility_building_count,
    b.trigger_status
   FROM (hazarded_aggregate_count
     LEFT JOIN public.village_trigger_status b ON (((b.village_id = hazarded_aggregate_count.village_id) AND (hazarded_aggregate_count.hazard_event_id = b.hazard_event_id))))
  WITH NO DATA;
