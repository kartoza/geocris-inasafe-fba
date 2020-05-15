drop function if exists kartoza_process_hazard_event_queue;
create or replace function kartoza_process_hazard_event_queue() returns
    table (
        hazard_event_id int
          )
    language plpgsql
as
    $$
    begin
        return query
            with new_hazard_event as (
                select *
                from hazard_event_queue
                where queue_status is null
                   or queue_status = 0
                limit 1
                ), delete_queue as (
                delete from hazard_event_queue where id in (select id from new_hazard_event) returning *
                )
                insert into hazard_event
                    (
                     hazard_map_id,
                     acquisition_date,
                     forecast_date,
                     source,
                     notes,
                     link,
                     trigger_status,
                     progress,
                     hazard_type_id
                        )
                    (select hazard_map_id,
                            acquisition_date,
                            forecast_date,
                            source,
                            notes,
                            link,
                            trigger_status,
                            1,
                            hazard_type_id
                     from delete_queue)
                    returning id;
    end
    $$;

-- include in cron
insert into cron.job (schedule, command, nodename, username)
select
    '*/5 * * * *', $$ select kartoza_process_hazard_event_queue() $$, '', 'postgres'
where
    not exists(
        select schedule, command, nodename, username from cron.job
        where schedule = '*/5 * * * *' and command = $$ select kartoza_process_hazard_event_queue() $$ and nodename = '' and username = 'postgres'
        );

insert into cron.job (schedule, command, nodename, username)
select
    '*/5 * * * *', $$ select kartoza_fba_forecast_glofas_update_trigger_status(id) from hazard_event where progress = 1 $$, '', 'postgres'
where
    not exists(
        select schedule, command, nodename, username from cron.job
        where schedule = '*/5 * * * *' and command = $$ select kartoza_fba_forecast_glofas_update_trigger_status(id) from hazard_event where progress = 1 $$ and nodename = '' and username = 'postgres'
        );
