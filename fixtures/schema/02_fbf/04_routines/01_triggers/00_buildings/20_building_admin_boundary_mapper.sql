CREATE OR REPLACE FUNCTION kartoza_building_admin_boundary_mapper() RETURNS trigger
    LANGUAGE plpgsql
AS $$
BEGIN
    SELECT
        v.village_code, s.sub_dc_code, d.dc_code
    INTO new.village_id, new.sub_district_id, new.district_id
    FROM village v
             JOIN sub_district s ON st_intersects(v.geom, s.geom)
             JOIN district d ON st_intersects(s.geom, d.geom)
    WHERE st_within(new.geometry, v.geom);
    RETURN NEW;
END
$$;
