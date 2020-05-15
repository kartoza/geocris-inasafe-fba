
--
-- Name: hazard_event_newest_forecast_f(timestamp without time zone, timestamp without time zone); Type: FUNCTION; Schema: public; Owner: -
--
DROP FUNCTION IF EXISTS public.hazard_event_newest_forecast_f;
CREATE FUNCTION public.hazard_event_newest_forecast_f(forecast_date_start timestamp without time zone, forecast_date_end timestamp without time zone) RETURNS TABLE(forecast_date_str text, acquisition_date_str text, trigger_status_id integer)
    LANGUAGE plpgsql
    AS $$
begin return query
        select distinct on (forecast_date_str) a.forecast_date_str, a.acquisition_date_str, a.trigger_status
        from (
            select id, to_char(forecast_date, 'YYYY-MM-DD') as forecast_date_str, to_char(acquisition_date, 'YYYY-MM-DD') as acquisition_date_str, trigger_status from hazard_event
            where forecast_date >= forecast_date_start and forecast_date < forecast_date_end AND forecast_date IS NOT NULL
 ) as a ORDER BY a.forecast_date_str DESC, a.acquisition_date_str DESC;
    end;
$$;
