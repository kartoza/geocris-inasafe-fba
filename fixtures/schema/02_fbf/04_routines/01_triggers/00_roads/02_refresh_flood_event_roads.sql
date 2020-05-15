
--
-- Name: kartoza_refresh_hazard_event_roads_mv(); Type: FUNCTION; Schema: public; Owner: -
--
DROP FUNCTION IF EXISTS public.kartoza_refresh_hazard_event_roads_mv CASCADE ;
CREATE FUNCTION public.kartoza_refresh_hazard_event_roads_mv() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
  BEGIN
    REFRESH MATERIALIZED VIEW mv_hazard_event_roads WITH DATA ;
    REFRESH MATERIALIZED VIEW mv_hazarded_roads_summary WITH DATA ;
    REFRESH MATERIALIZED VIEW mv_hazard_event_road_village_summary WITH DATA ;
    REFRESH MATERIALIZED VIEW mv_hazard_event_road_sub_district_summary WITH DATA ;
    REFRESH MATERIALIZED VIEW mv_hazard_event_road_district_summary WITH DATA ;
    RETURN NULL;
  END
  $$;
