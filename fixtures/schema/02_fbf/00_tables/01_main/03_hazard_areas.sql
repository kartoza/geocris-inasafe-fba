--
-- Name: hazard_areas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS public.hazard_areas (
    id integer NOT NULL,
    hazard_map_id integer,
    hazarded_area_id integer,
    CONSTRAINT hazarded_areas_pkey PRIMARY KEY (id),
    CONSTRAINT hazarded_areas_hazard_map_id_fkey FOREIGN KEY (hazard_map_id) REFERENCES public.hazard_map(id),
    CONSTRAINT hazarded_areas_hazarded_area_id_fkey FOREIGN KEY (hazarded_area_id) REFERENCES public.hazard_area(id)
);


--
-- Name: hazarded_areas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE IF NOT EXISTS public.hazarded_areas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hazarded_areas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.hazarded_areas_id_seq OWNED BY public.hazard_areas.id;

--
-- Name: hazard_areas id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hazard_areas ALTER COLUMN id SET DEFAULT nextval('public.hazarded_areas_id_seq'::regclass);
