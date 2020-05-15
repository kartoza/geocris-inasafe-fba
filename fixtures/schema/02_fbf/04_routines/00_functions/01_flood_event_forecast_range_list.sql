
--
-- Name: hazard_event_forecast_range_list_f(timestamp without time zone, timestamp without time zone); Type: FUNCTION; Schema: public; Owner: -
--
DROP FUNCTION IF EXISTS public.hazard_event_forecast_range_list_f;
CREATE FUNCTION public.hazard_event_forecast_range_list_f(acquisition_date_start timestamp without time zone, acquisition_date_end timestamp without time zone) RETURNS TABLE(total_forecast bigint, forecast_date_str text, acquisition_date_str text, trigger_status_id integer)
    LANGUAGE plpgsql
    AS $$
begin return query
         select count(a.id) as total_forecast,
               a.forecast_date_str as forecast_date_str,
               a.acquisition_date_str as acquisition_date_str, MAX(a.trigger_status) as trigger_status_id
        from (
            select id, to_char(forecast_date, 'YYYY-MM-DD') as forecast_date_str, to_char(acquisition_date, 'YYYY-MM-DD') as acquisition_date_str, trigger_status from hazard_event
            where (acquisition_date >= acquisition_date_start and acquisition_date < acquisition_date_end AND forecast_date IS NOT NULL)
 ) as a
        group by a.forecast_date_str, a.acquisition_date_str ORDER BY a.acquisition_date_str;
    end;
$$;
