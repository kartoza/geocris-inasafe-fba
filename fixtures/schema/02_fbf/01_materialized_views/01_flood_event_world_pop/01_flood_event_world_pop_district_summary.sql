drop materialized view if exists mv_flood_event_world_pop_district_summary;
create materialized view mv_flood_event_world_pop_district_summary as
with flooded_count as (
select
    flood_event_id,
    a.dc_code,
    b.name,
    round(sum(pop_sum)) as flooded_population_count
from (
    select
        flood_event_id,
        dc_code,
        sum(pop_sum) as pop_sum
    from mv_flood_event_world_pop
        where depth_class > 2
    group by flood_event_id, dc_code, depth_class) a
    join district b on a.dc_code = b.dc_code
group by flood_event_id, a.dc_code, b.name)
    select
        row_number() over () as id,
        a.flood_event_id,
        a.dc_code as district_id,
        a.name,
        round(b.pop_sum) as population_count,
        a.flooded_population_count,
        c.trigger_status
    from flooded_count a
    join world_pop_district_stats b on a.dc_code = b.dc_code
    left join district_trigger_status c on a.flood_event_id = c.flood_event_id and a.dc_code = c.district_id
WITH NO DATA;

CREATE UNIQUE INDEX IF NOT EXISTS mv_flood_event_world_pop_district_summary ON
    mv_flood_event_world_pop_district_summary(id)
