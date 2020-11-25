--
-- Name: vw_country_extent; Type: VIEW; Schema: public; Owner: -
--

CREATE OR REPLACE VIEW public.vw_country_extent AS
 SELECT country_extent.id,
    country_extent.id_code,
    public.st_xmin((country_extent.extent)::public.box3d) AS x_min,
    public.st_ymin((country_extent.extent)::public.box3d) AS y_min,
    public.st_xmax((country_extent.extent)::public.box3d) AS x_max,
    public.st_ymax((country_extent.extent)::public.box3d) AS y_max
   FROM ( SELECT country.id,
            country.country_code AS id_code,
            public.st_extent(country.geom) AS extent
           FROM public.country
          GROUP BY country.id, country.country_code) country_extent;
