drop materialized view if exists mv_hazard_event_world_pop_village_summary;
create materialized view mv_hazard_event_world_pop_village_summary as
with hazarded_count as (
select
    hazard_event_id,
    a.dc_code,
    a.sub_dc_code,
    a.village_code,
    b.name,
    round(sum(pop_sum)) as hazarded_population_count
from (
    select
        hazard_event_id,
        dc_code,
        sub_dc_code,
        village_code,
        sum(pop_sum) as pop_sum
    from mv_hazard_event_world_pop
        where hazard_class > 2
    group by hazard_event_id, dc_code, sub_dc_code, village_code, hazard_class) a
    join village b on a.village_code = b.village_code
group by hazard_event_id, a.dc_code, a.sub_dc_code, a.village_code, b.name)
    select
        a.hazard_event_id,
        a.dc_code as district_id,
        a.sub_dc_code as sub_district_id,
        a.village_code as village_id,
        a.name,
        round(b.pop_sum) as population_count,
        a.hazarded_population_count,
        c.trigger_status
    from hazarded_count a
    join world_pop_village_stats b on a.village_code = b.village_code
    left join village_trigger_status c on a.hazard_event_id = c.hazard_event_id and a.village_code = c.village_id
WITH NO DATA;
