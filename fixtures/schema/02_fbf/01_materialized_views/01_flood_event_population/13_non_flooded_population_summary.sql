DROP MATERIALIZED VIEW IF EXISTS public.mv_population_summary;
CREATE MATERIALIZED VIEW public.mv_population_summary AS
    select
           a.district_id,
           a.sub_district_id,
           a.village_id,
           c.population,
           c.males,
           c.females,
           c.elderly,
           c.unemployed
    from census c join mv_administrative_mapping a on c.village_id = a.village_id
    order by a.district_id, a.sub_district_id, a.village_id
  WITH NO DATA;

