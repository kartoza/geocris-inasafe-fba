DROP FUNCTION IF EXISTS public.hazard_event_forecast_list_f;
-- TODO:
-- Remove acquisition_date_end and sync the request parameter with frontend
CREATE OR REPLACE FUNCTION public.hazard_event_forecast_list_f(acquisition_date_start timestamp without time zone, acquisition_date_end timestamp without time zone) RETURNS TABLE(total_forecast bigint, max_acquisition_date timestamp without time zone, lead_time bigint, trigger_status_id integer)
    LANGUAGE plpgsql
    AS $$
begin return query
        select count(a.id) as total_forecast,
               max(a.acquisition_date) as max_acquisition_date,
               a.lead_time, MAX(a.trigger_status) as trigger_status_id
        from (
            select id,
                   acquisition_date,
                   extract(day from forecast_date - acquisition_date)::bigint as lead_time, trigger_status
            from hazard_event
            where (
                forecast_date >= acquisition_date_start)
            ) as a
        group by a.lead_time;
    end;
$$;
