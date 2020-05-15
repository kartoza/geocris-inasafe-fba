DROP MATERIALIZED VIEW IF EXISTS public.mv_hazard_event_population_village_summary;
CREATE MATERIALIZED VIEW public.mv_hazard_event_population_village_summary AS
    WITH non_hazarded_count as (
        select
               a.district_id,
               a.sub_district_id,
               a.village_id,
               sum(a.population) as population_count,
               sum(a.males) as males_population_count,
               sum(a.females) as females_population_count,
               sum(a.elderly) as elderly_population_count,
               sum(a.unemployed) as unemployed_population_count
        from mv_population_summary a
        where a.district_id is not null and a.sub_district_id is not null and a.village_id is not null
        group by a.district_id, a.sub_district_id, a.village_id
    ), hazarded_count as (
        select
                a.hazard_event_id,
                a.district_id,
                a.sub_district_id,
                a.village_id,
                sum(a.population) as hazarded_population_count,
                sum(a.males) as males_hazarded_population_count,
                sum(a.females) as females_hazarded_population_count,
                sum(a.elderly) as elderly_hazarded_population_count,
                sum(a.unemployed) as unemployed_hazarded_population_count
        from mv_hazard_event_population a
        where a.district_id is not null and a.sub_district_id is not null and a.village_id is not null
        group by a.hazard_event_id, a.district_id, a.sub_district_id, a.village_id
        )
    select
           hazarded_count.hazard_event_id,
           hazarded_count.district_id,
           hazarded_count.sub_district_id,
           hazarded_count.village_id,
           region.name,
           non_hazarded_count.population_count,
           hazarded_count.hazarded_population_count,
           hazarded_count.males_hazarded_population_count,
           hazarded_count.females_hazarded_population_count,
           hazarded_count.elderly_hazarded_population_count,
           hazarded_count.unemployed_hazarded_population_count,
           non_hazarded_count.males_population_count,
           non_hazarded_count.females_population_count,
           non_hazarded_count.elderly_population_count,
           non_hazarded_count.unemployed_population_count,
           trigger_status.trigger_status
    from
         hazarded_count
         LEFT JOIN village_trigger_status trigger_status on hazarded_count.hazard_event_id = trigger_status.hazard_event_id and hazarded_count.village_id = trigger_status.village_id
         JOIN non_hazarded_count on hazarded_count.village_id = non_hazarded_count.village_id
         JOIN village region on hazarded_count.village_id = region.village_code
  WITH NO DATA;

