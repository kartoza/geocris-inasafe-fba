
--
-- Name: kartoza_refresh_hazard_event_buildings_mv(); Type: FUNCTION; Schema: public; Owner: -
--
DROP FUNCTION IF EXISTS public.kartoza_refresh_hazard_event_buildings_mv CASCADE ;
CREATE FUNCTION public.kartoza_refresh_hazard_event_buildings_mv() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
  BEGIN
    REFRESH MATERIALIZED VIEW mv_hazard_event_buildings WITH DATA ;
    REFRESH MATERIALIZED VIEW mv_hazarded_building_summary WITH DATA ;
    REFRESH MATERIALIZED VIEW mv_hazard_event_village_summary WITH DATA ;
    REFRESH MATERIALIZED VIEW mv_hazard_event_sub_district_summary WITH DATA ;
    REFRESH MATERIALIZED VIEW mv_hazard_event_district_summary WITH DATA ;
    RETURN NULL;
  END
  $$;
