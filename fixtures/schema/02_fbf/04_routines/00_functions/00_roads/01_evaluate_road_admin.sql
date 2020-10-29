CREATE OR REPLACE FUNCTION public.kartoza_evaluate_road_admin() RETURNS VARCHAR
    LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE osm_roads
    SET
        village_id = res.village_id,
        sub_district_id = res.sub_district_id,
        district_id = res.district_id
    FROM
         (select osm_id, village_id, sub_district_id, district_id
                from
            (select * from osm_roads where village_id is null) b
                JOIN village v ON st_within(b.geometry, v.geom)
                 JOIN sub_district s ON st_intersects(v.geom, s.geom)
                 JOIN district d ON st_intersects(s.geom, d.geom)) res
    WHERE res.osm_id = osm_roads.osm_id;
    RETURN 'OK';
END
$$;
