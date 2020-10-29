DROP MATERIALIZED VIEW IF EXISTS public.mv_flood_event_population_country_summary;
CREATE MATERIALIZED VIEW public.mv_flood_event_population_country_summary AS
 WITH flooded_count AS (
     SELECT
        c.country_code as country_id,
        c.name as country_name,
        a.*
     FROM mv_flood_event_population_district_summary a
     JOIN district d on a.district_id = d.dc_code
     JOIN country c on d.country_code = c.country_code
 )
    select
           row_number() over () as id,
           flooded_count.flood_event_id,
           flooded_count.country_id,
           flooded_count.country_name as name,
           sum(flooded_count.population_count) as population_count,
           sum(flooded_count.flooded_population_count) as flooded_population_count,
           sum(flooded_count.males_flooded_population_count) as males_flooded_population_count,
           sum(flooded_count.females_flooded_population_count) as females_flooded_population_count,
           sum(flooded_count.elderly_flooded_population_count) as elderly_flooded_population_count,
           sum(flooded_count.unemployed_flooded_population_count) as unemployed_flooded_population_count,
           sum(flooded_count.males_population_count) as males_population_count,
           sum(flooded_count.females_population_count) as females_population_count,
           sum(flooded_count.elderly_population_count) as elderly_population_count,
           sum(flooded_count.unemployed_population_count) as unemployed_population_count,
           max(flooded_count.trigger_status) as trigger_status
    from
         flooded_count
   GROUP BY flood_event_id, country_id, country_name
  WITH NO DATA;

CREATE UNIQUE INDEX IF NOT EXISTS mv_flood_event_population_country_summary_idx ON
    mv_flood_event_population_country_summary(id)
