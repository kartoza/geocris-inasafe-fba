
--
-- Name: kartoza_populate_spreadsheet_table(); Type: FUNCTION; Schema: public; Owner: -
--
DROP FUNCTION IF EXISTS public.kartoza_populate_spreadsheet_table CASCADE;
CREATE FUNCTION public.kartoza_populate_spreadsheet_table() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
  BEGIN
    insert into spreadsheet_reports (hazard_event_id)
    values (NEW.id);
    RETURN NEW;
  END
  $$;

