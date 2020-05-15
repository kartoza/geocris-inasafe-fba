
CREATE OR REPLACE FUNCTION public.kartoza_refresh_hazard_event_world_pop_mv() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
  BEGIN
    REFRESH MATERIALIZED VIEW mv_hazard_event_world_pop WITH DATA ;
    REFRESH MATERIALIZED VIEW mv_hazard_event_world_pop_village_summary WITH DATA ;
    REFRESH MATERIALIZED VIEW mv_hazard_event_world_pop_sub_district_summary WITH DATA ;
    REFRESH MATERIALIZED VIEW mv_hazard_event_world_pop_district_summary WITH DATA ;
    RETURN NULL;
  END
  $$;
