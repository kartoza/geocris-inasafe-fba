--
-- Name: hazard_area; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS public.hazard_area (
    id integer NOT NULL,
    hazard_class integer,
    geometry public.geometry(MultiPolygon,4326),
    CONSTRAINT hazarded_area_hazard_class_fkey FOREIGN KEY (hazard_class) REFERENCES public.hazard_class(id),
    CONSTRAINT hazarded_area_pkey PRIMARY KEY (id)
);


--
-- Name: hazarded_area_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE IF NOT EXISTS public.hazarded_area_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hazarded_area_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.hazarded_area_id_seq OWNED BY public.hazard_area.id;

--
-- Name: hazard_area id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hazard_area ALTER COLUMN id SET DEFAULT nextval('public.hazarded_area_id_seq'::regclass);


--
-- Name: hazarded_area_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX IF NOT EXISTS hazarded_area_id ON public.hazard_area USING btree (id);

--
-- Name: hazarded_area_idx_geometry; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX IF NOT EXISTS hazarded_area_idx_geometry ON public.hazard_area USING gist (geometry);
