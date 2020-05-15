
--
-- Name: kartoza_refresh_building_summary_mv(); Type: FUNCTION; Schema: public; Owner: -
--
DROP FUNCTION IF EXISTS public.kartoza_refresh_building_summary_mv CASCADE ;
CREATE FUNCTION public.kartoza_refresh_building_summary_mv() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
  BEGIN
    REFRESH MATERIALIZED VIEW  mv_building_summary WITH DATA ;
    RETURN NULL;
  END
  $$;
