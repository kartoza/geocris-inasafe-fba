create or replace view vw_village_impact
            (hazard_event_id, district_id, sub_district_id, village_id,
             impact_ratio) as
WITH total_village_count_table AS (
    SELECT mv_building_summary.district_id,
           mv_building_summary.sub_district_id,
           mv_building_summary.village_id,
           sum(
                   mv_building_summary.building_type_count) AS total_building
    FROM mv_building_summary
    WHERE mv_building_summary.district_id IS NOT NULL
      AND mv_building_summary.sub_district_id IS NOT NULL
      AND mv_building_summary.village_id IS NOT NULL
    GROUP BY mv_building_summary.district_id,
             mv_building_summary.sub_district_id,
             mv_building_summary.village_id
),
     building_filter AS (
         SELECT mv_hazard_event_buildings.hazard_event_id,
                mv_hazard_event_buildings.district_id,
                mv_hazard_event_buildings.sub_district_id,
                mv_hazard_event_buildings.village_id,
                mv_hazard_event_buildings.building_id,
                max(mv_hazard_event_buildings.hazard_class)             AS hazard_class,
                max(
                        mv_hazard_event_buildings.total_vulnerability) AS total_vulnerability
         FROM mv_hazard_event_buildings
         WHERE mv_hazard_event_buildings.district_id IS NOT NULL
           AND mv_hazard_event_buildings.sub_district_id IS NOT NULL
           AND mv_hazard_event_buildings.village_id IS NOT NULL
         GROUP BY mv_hazard_event_buildings.hazard_event_id,
                  mv_hazard_event_buildings.district_id,
                  mv_hazard_event_buildings.sub_district_id,
                  mv_hazard_event_buildings.village_id,
                  mv_hazard_event_buildings.building_id
     ),
     impact_count AS (
         SELECT building_filter.hazard_event_id,
                building_filter.village_id,
                CASE
                    WHEN building_filter.hazard_class = 2 AND
                         building_filter.total_vulnerability > 0.6 THEN 1
                    WHEN building_filter.hazard_class = 3 AND
                         building_filter.total_vulnerability > 0.3 THEN 1
                    WHEN building_filter.hazard_class = 4 AND
                         building_filter.total_vulnerability > 0::numeric
                        THEN 1
                    ELSE 0
                    END AS impacted_count
         FROM building_filter
     ),
     impact_sum AS (
         SELECT impact_count.hazard_event_id,
                impact_count.village_id,
                sum(impact_count.impacted_count) AS total_impact
         FROM impact_count
         GROUP BY impact_count.hazard_event_id, impact_count.village_id
     )
SELECT impact_sum.hazard_event_id,
       total_village_count_table.district_id,
       total_village_count_table.sub_district_id,
       impact_sum.village_id,
       impact_sum.total_impact::numeric /
       total_village_count_table.total_building AS impact_ratio
FROM total_village_count_table
         JOIN impact_sum ON impact_sum.village_id =
                            total_village_count_table.village_id AND
                            total_village_count_table.total_building >
                            0::numeric;
