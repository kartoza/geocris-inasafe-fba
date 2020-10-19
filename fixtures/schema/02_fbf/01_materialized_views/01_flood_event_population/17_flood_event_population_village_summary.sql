DROP MATERIALIZED VIEW IF EXISTS public.mv_flood_event_population_village_summary;
CREATE MATERIALIZED VIEW public.mv_flood_event_population_village_summary AS
    WITH non_flooded_count as (
        select
               a.district_id,
               a.sub_district_id,
               a.village_id,
               sum(a.population) as population_count,
               sum(a.males) as males_population_count,
               sum(a.females) as females_population_count,
               sum(a.elderly) as elderly_population_count,
               sum(a.unemployed) as unemployed_population_count
        from mv_non_flooded_population_summary a
        where a.district_id is not null and a.sub_district_id is not null and a.village_id is not null
        group by a.district_id, a.sub_district_id, a.village_id
    ), flooded_count as (
        select
                a.flood_event_id,
                a.district_id,
                a.sub_district_id,
                a.village_id,
                sum(a.population) as flooded_population_count,
                sum(a.males) as males_flooded_population_count,
                sum(a.females) as females_flooded_population_count,
                sum(a.elderly) as elderly_flooded_population_count,
                sum(a.unemployed) as unemployed_flooded_population_count
        from mv_flood_event_population a
        where a.district_id is not null and a.sub_district_id is not null and a.village_id is not null
        group by a.flood_event_id, a.district_id, a.sub_district_id, a.village_id
        )
    select
           row_number() over () as id,
           flooded_count.flood_event_id,
           flooded_count.district_id,
           flooded_count.sub_district_id,
           flooded_count.village_id,
           region.name,
           non_flooded_count.population_count,
           flooded_count.flooded_population_count,
           flooded_count.males_flooded_population_count,
           flooded_count.females_flooded_population_count,
           flooded_count.elderly_flooded_population_count,
           flooded_count.unemployed_flooded_population_count,
           non_flooded_count.males_population_count,
           non_flooded_count.females_population_count,
           non_flooded_count.elderly_population_count,
           non_flooded_count.unemployed_population_count,
           trigger_status.trigger_status
    from
         flooded_count
         LEFT JOIN village_trigger_status trigger_status on flooded_count.flood_event_id = trigger_status.flood_event_id and flooded_count.village_id = trigger_status.village_id
         JOIN non_flooded_count on flooded_count.village_id = non_flooded_count.village_id
         JOIN village region on flooded_count.village_id = region.village_code
  WITH NO DATA;

CREATE UNIQUE INDEX IF NOT EXISTS mv_flood_event_population_village_summary ON
    mv_flood_event_population_village_summary(id)
