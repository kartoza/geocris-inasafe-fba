drop materialized view if exists mv_hazard_event_world_pop cascade ;
create materialized view mv_hazard_event_world_pop as
WITH hazard_intersections AS (
        SELECT st_makevalid(a_1.geometry) as geometry,
               d_1.id AS hazard_event_id,
               a_1.hazard_class
        FROM hazard_area a_1
                 JOIN hazard_areas b_1 ON a_1.id = b_1.hazarded_area_id
                 JOIN hazard_map c ON c.id = b_1.hazard_map_id
                 JOIN hazard_event d_1 ON d_1.hazard_map_id = c.id
    ),
     hazard_admin_intersections AS (
         SELECT st_makevalid(st_intersection(a.geometry, st_makevalid(b.geom))) AS geometry,
                a.hazard_event_id,
                a.hazard_class,
                b.dc_code,
                b.sub_dc_code,
                b.village_code
         FROM hazard_intersections a
                  JOIN village b ON st_intersects(a.geometry, b.geom)
     ),
     stats as (
         SELECT row_number() OVER ()                                     AS id,
                st_summarystatsagg(st_clip(b.rast, a.geometry), 1,
                                   true)                                 AS stats,
                a.hazard_event_id,
                a.hazard_class,
                a.geometry,
                a.dc_code,
                a.sub_dc_code,
                a.village_code
         FROM hazard_admin_intersections a
                  JOIN world_pop b ON  st_intersects(b.rast, a.geometry)
         GROUP BY a.hazard_event_id, a.hazard_class, a.geometry, a.dc_code,
                  a.sub_dc_code, a.village_code
     )
SELECT d.id,
       (d.stats).count as pop_count,
       (d.stats).sum as pop_sum,
       (d.stats).mean as pop_mean,
       (d.stats).stddev as pop_sttdev,
       (d.stats).min as pop_min,
       (d.stats).max as pop_max,
       d.hazard_event_id,
       d.hazard_class,
       d.geometry,
       d.dc_code,
       d.sub_dc_code,
       d.village_code
FROM stats d
WITH NO DATA;

comment on materialized view mv_hazard_event_world_pop is 'This gives a summary of the population for each hazard zone in a village region. It doesn''t aggregate per region';

create unique index if not exists mv_hazard_event_world_pop_uidx on mv_hazard_event_world_pop(id);

create index if not exists mv_hazard_event_world_pop_sidx_geometry on mv_hazard_event_world_pop using gist (geometry);
