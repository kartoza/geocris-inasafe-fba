--
-- Name: mv_administrative_mapping; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--
DROP MATERIALIZED VIEW IF EXISTS public.mv_administrative_mapping cascade;
CREATE MATERIALIZED VIEW public.mv_administrative_mapping AS
select
       a.country_id,
       a.country_name,
       a.district_id,
       a.district_name,
       a.sub_district_id,
       a.sub_district_name,
       a.village_id,
       a.village_name
from (SELECT
             country.country_code                     AS country_id,
             country.name                             AS country_name,
             district.dc_code                         AS district_id,
             district.name                            AS district_name,
             sub_district.sub_dc_code                 AS sub_district_id,
             sub_district.name                        AS sub_district_name,
             village.village_code                     AS village_id,
             village.name                             AS village_name,
             row_number() over (partition by
                 country.name, district.name, sub_district.name, village.name
                 order by village.village_code DESC ) as row_number
      FROM
           country
               LEFT JOIN district ON
                   country.country_code = district.country_code::double precision
               LEFT JOIN sub_district ON
                   district.dc_code = sub_district.dc_code::double precision
               LEFT JOIN village ON
                   village.sub_dc_code = sub_district.sub_dc_code::double precision
    ) a
where a.row_number = 1
    WITH NO DATA;

create unique index if not exists mv_administrative_mapping_uindex
    on mv_administrative_mapping(district_id, sub_district_id, village_id)
