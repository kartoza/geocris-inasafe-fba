drop materialized view if exists mv_flood_event_world_pop_village_summary;
create materialized view mv_flood_event_world_pop_village_summary as
with flooded_count as (
select
    flood_event_id,
    a.dc_code,
    a.sub_dc_code,
    a.village_code,
    b.name,
    round(sum(pop_sum)) as flooded_population_count
from (
    select
        flood_event_id,
        dc_code,
        sub_dc_code,
        village_code,
        sum(pop_sum) as pop_sum
    from mv_flood_event_world_pop
        where depth_class > 2
    group by flood_event_id, dc_code, sub_dc_code, village_code, depth_class) a
    join village b on a.village_code = b.village_code
group by flood_event_id, a.dc_code, a.sub_dc_code, a.village_code, b.name)
    select
        row_number() over () as id,
        a.flood_event_id,
        a.dc_code as district_id,
        a.sub_dc_code as sub_district_id,
        a.village_code as village_id,
        a.name,
        round(b.pop_sum) as population_count,
        a.flooded_population_count,
        c.trigger_status
    from flooded_count a
    join world_pop_village_stats b on a.village_code = b.village_code
    left join village_trigger_status c on a.flood_event_id = c.flood_event_id and a.village_code = c.village_id
WITH NO DATA;

CREATE UNIQUE INDEX IF NOT EXISTS mv_flood_event_world_pop_village_summary ON
    mv_flood_event_world_pop_village_summary(id)
