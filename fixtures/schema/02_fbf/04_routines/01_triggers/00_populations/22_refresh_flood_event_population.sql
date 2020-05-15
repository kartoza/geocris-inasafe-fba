
CREATE OR REPLACE FUNCTION public.kartoza_refresh_hazard_event_population_mv() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
  BEGIN
    REFRESH MATERIALIZED VIEW mv_hazard_event_population WITH DATA ;
    REFRESH MATERIALIZED VIEW mv_hazard_event_population_village_summary WITH DATA ;
    REFRESH MATERIALIZED VIEW mv_hazard_event_population_sub_district_summary WITH DATA ;
    REFRESH MATERIALIZED VIEW mv_hazard_event_population_district_summary WITH DATA ;
    RETURN NULL;
  END
  $$;
