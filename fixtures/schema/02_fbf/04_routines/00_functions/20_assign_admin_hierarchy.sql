create or replace function kartoza_fba_assign_admin_hierarchy() returns character varying
    language plpgsql
as
$$
BEGIN
update district set country_code = country.country_code from country where st_intersects(district.geom, country.geom);
update sub_district set dc_code = district.dc_code from district where st_intersects(sub_district.geom, district.geom);
update village set dc_code = sub_district.dc_code, sub_dc_code = sub_district.sub_dc_code from sub_district where st_intersects(village.geom, sub_district.geom);
refresh materialized view mv_administrative_mapping with data;
refresh materialized view mv_non_flooded_population_summary with data;
refresh materialized view mv_non_flooded_building_summary with data;
refresh materialized view mv_non_flooded_roads_summary with data;

RETURN 'OK';
END
$$;

