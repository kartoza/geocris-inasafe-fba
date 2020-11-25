create or replace view vw_administrative_country_mapping_country_filter
            (country_id, country_name) as
select distinct country_id, country_name from mv_administrative_mapping;

create or replace view vw_administrative_country_mapping_district_filter
            (country_id, country_name, district_id) as
select distinct country_id, country_name, district_id from mv_administrative_mapping;

create or replace view vw_administrative_country_mapping_sub_district_filter
            (country_id, country_name, sub_district_id) as
select distinct country_id, country_name, sub_district_id from mv_administrative_mapping;

create or replace view vw_administrative_country_mapping_village_filter
            (country_id, country_name, village_id) as
select distinct country_id, country_name, village_id from mv_administrative_mapping;
