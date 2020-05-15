
--
-- Name: hazard_event_historical_forecast_list_f(timestamp without time zone, timestamp without time zone); Type: FUNCTION; Schema: public; Owner: -
--
DROP FUNCTION IF EXISTS public.hazard_event_historical_forecast_list_f;
CREATE FUNCTION public.hazard_event_historical_forecast_list_f(forecast_date_range_start timestamp without time zone, forecast_date_range_end timestamp without time zone) RETURNS TABLE(total_forecast bigint, relative_forecast_date bigint, minimum_lead_time bigint, maximum_lead_time bigint, trigger_status_id integer)
    LANGUAGE plpgsql
    AS $$
begin return query
--         historical forecast only
    select
        count(a.id) as total_forecast,
        a.relative_forecast_date,
        min(a.lead_time) as minimum_lead_time,
        max(a.lead_time) as maximum_lead_time,
        max(a.trigger_status) as trigger_status_id
    from
    (select
        hazard_event.id,
           extract(day from forecast_date - forecast_date_range_start)::bigint as relative_forecast_date,
            extract(day from forecast_date - acquisition_date)::bigint as lead_time,
        hazard_event.trigger_status
    from hazard_event
    where forecast_date >= forecast_date_range_start and forecast_date < forecast_date_range_end) as a
    group by a.relative_forecast_date;
    end;
$$;
