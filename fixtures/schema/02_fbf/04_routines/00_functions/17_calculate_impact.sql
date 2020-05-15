create or replace function kartoza_calculate_impact() returns character varying
    language plpgsql
as
$$
BEGIN
refresh materialized view mv_hazard_event_buildings with data;
refresh materialized view mv_hazarded_building_summary with data;
refresh materialized view mv_hazard_event_village_summary with data;
refresh materialized view mv_hazard_event_sub_district_summary with data;
refresh materialized view mv_hazard_event_district_summary with data;


refresh materialized view mv_hazard_event_roads with data;
refresh materialized view mv_hazarded_roads_summary with data;
refresh materialized view mv_hazard_event_road_village_summary with data;
refresh materialized view mv_hazard_event_road_sub_district_summary with data;
refresh materialized view mv_hazard_event_road_district_summary with data;

refresh materialized view mv_hazard_event_population with data;
refresh materialized view mv_hazard_event_population_village_summary with data;
refresh materialized view mv_hazard_event_population_sub_district_summary with data;
refresh materialized view mv_hazard_event_population_district_summary with data;

refresh materialized view mv_hazard_event_world_pop with data;
refresh materialized view mv_hazard_event_world_pop_village_summary with data;
refresh materialized view mv_hazard_event_world_pop_sub_district_summary with data;
refresh materialized view mv_hazard_event_world_pop_district_summary with data;

RETURN 'OK';
END
$$;

