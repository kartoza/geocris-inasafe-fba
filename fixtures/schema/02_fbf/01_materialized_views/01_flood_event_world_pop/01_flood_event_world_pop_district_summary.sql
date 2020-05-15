drop materialized view if exists mv_hazard_event_world_pop_district_summary;
create materialized view mv_hazard_event_world_pop_district_summary as
with hazarded_count as (
select
    hazard_event_id,
    a.dc_code,
    b.name,
    round(sum(pop_sum)) as hazarded_population_count
from (
    select
        hazard_event_id,
        dc_code,
        sum(pop_sum) as pop_sum
    from mv_hazard_event_world_pop
        where hazard_class > 2
    group by hazard_event_id, dc_code, hazard_class) a
    join district b on a.dc_code = b.dc_code
group by hazard_event_id, a.dc_code, b.name)
    select
        a.hazard_event_id,
        a.dc_code as district_id,
        a.name,
        round(b.pop_sum) as population_count,
        a.hazarded_population_count,
        c.trigger_status
    from hazarded_count a
    join world_pop_district_stats b on a.dc_code = b.dc_code
    left join district_trigger_status c on a.hazard_event_id = c.hazard_event_id and a.dc_code = c.district_id
WITH NO DATA;
