
DROP MATERIALIZED VIEW IF EXISTS public.mv_hazard_event_population CASCADE;
CREATE MATERIALIZED VIEW public.mv_hazard_event_population AS
 WITH intersections AS (
         SELECT a_1.geometry,
            d.id AS hazard_event_id,
            a_1.hazard_class
           FROM (((public.hazard_area a_1
             JOIN public.hazard_areas b_1 ON ((a_1.id = b_1.hazarded_area_id)))
             JOIN public.hazard_map c ON ((c.id = b_1.hazard_map_id)))
             JOIN public.hazard_event d ON ((d.hazard_map_id = c.id)))
        ),
      admin_boundaries as (
          select
              a.hazard_event_id,
              max(a.hazard_class) as hazard_class,
              d.district_id,
              d.sub_district_id,
              d.village_id,
              st_union(b.geom) as geometry
          from intersections a
            JOIN village b ON st_intersects(a.geometry, b.geom)
            JOIN mv_administrative_mapping d ON b.village_code = d.village_id
          GROUP BY a.hazard_event_id, d.district_id, d.sub_district_id, d.village_id
      )
 SELECT row_number() OVER () AS id,
        a.*,
        c.population,
        c.males,
        c.females,
        c.elderly,
        c.unemployed
   FROM admin_boundaries a
     JOIN census c ON a.village_id = c.village_id
  WITH NO DATA;
