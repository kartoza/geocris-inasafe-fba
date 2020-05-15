--
-- Name: vw_hazard_event_extent; Type: VIEW; Schema: public; Owner: -
--

CREATE OR REPLACE VIEW public.vw_hazard_event_extent AS
 SELECT hazard_extent.id,
    public.st_xmin((hazard_extent.extent)::public.box3d) AS x_min,
    public.st_ymin((hazard_extent.extent)::public.box3d) AS y_min,
    public.st_xmax((hazard_extent.extent)::public.box3d) AS x_max,
    public.st_ymax((hazard_extent.extent)::public.box3d) AS y_max
   FROM ( SELECT hazard_event.id,
            public.st_extent(hazard_area.geometry) AS extent
           FROM (((public.hazard_event
             JOIN public.hazard_map ON ((hazard_event.hazard_map_id = hazard_map.id)))
             JOIN public.hazard_areas ON ((hazard_map.id = hazard_areas.hazard_map_id)))
             JOIN public.hazard_area ON ((hazard_areas.hazarded_area_id = hazard_area.id)))
          GROUP BY hazard_event.id) hazard_extent;

