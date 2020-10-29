create or replace function kartoza_calculate_impact() returns character varying
    language plpgsql
as
$$
BEGIN
refresh materialized view mv_non_flooded_building_summary with data;
refresh materialized view mv_non_flooded_roads_summary with data;
refresh materialized view mv_non_flooded_population_summary with data;

refresh materialized view mv_flood_event_buildings with data;
refresh materialized view mv_flooded_building_summary with data;
refresh materialized view mv_flood_event_village_summary with data;
refresh materialized view mv_flood_event_sub_district_summary with data;
refresh materialized view mv_flood_event_district_summary with data;
refresh materialized view mv_flood_event_country_summary with data;


refresh materialized view mv_flood_event_roads with data;
refresh materialized view mv_flooded_roads_summary with data;
refresh materialized view mv_flood_event_road_village_summary with data;
refresh materialized view mv_flood_event_road_sub_district_summary with data;
refresh materialized view mv_flood_event_road_district_summary with data;
refresh materialized view mv_flood_event_road_country_summary with data;

refresh materialized view mv_flood_event_population with data;
refresh materialized view mv_flood_event_population_village_summary with data;
refresh materialized view mv_flood_event_population_sub_district_summary with data;
refresh materialized view mv_flood_event_population_district_summary with data;
refresh materialized view mv_flood_event_population_country_summary with data;

refresh materialized view mv_flood_event_world_pop with data;
refresh materialized view mv_flood_event_world_pop_village_summary with data;
refresh materialized view mv_flood_event_world_pop_sub_district_summary with data;
refresh materialized view mv_flood_event_world_pop_district_summary with data;

RETURN 'OK';
END
$$;

