--
-- Name: vw_hazard_event_areas; Type: VIEW; Schema: public; Owner: -
--

CREATE OR REPLACE VIEW public.vw_hazard_event_areas AS
 SELECT a.geometry,
    d.id AS hazard_event_id,
    c.id AS hazard_map_id,
    a.hazard_class
   FROM (((public.hazard_area a
     JOIN public.hazard_areas b ON ((a.id = b.hazarded_area_id)))
     JOIN public.hazard_map c ON ((c.id = b.hazard_map_id)))
     JOIN public.hazard_event d ON ((d.hazard_map_id = c.id)));

