--
-- Name: hazard; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS public.hazard (
    id integer NOT NULL,
    geometry public.geometry(MultiPolygon,4326),
    name character varying(80),
    source character varying(255),
    reporting_date_time timestamp without time zone,
    forecast_date_time timestamp without time zone,
    station character varying(255),
    constraint hazard_event_pkey primary key (id)
);

--
-- Name: osm_hazard_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE IF NOT EXISTS public.osm_hazard_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: hazard id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hazard ALTER COLUMN id SET DEFAULT nextval('public.osm_hazard_id_seq'::regclass);

--
-- Name: osm_hazard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.osm_hazard_id_seq OWNED BY public.hazard.id;

-- Name: id_osm_hazard_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX IF NOT EXISTS id_osm_hazard_idx ON public.hazard USING btree (id);


--
-- Name: id_osm_hazard_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX IF NOT EXISTS id_osm_hazard_name ON public.hazard USING btree (name);


--
-- Name: osm_hazard_gix; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX IF NOT EXISTS osm_hazard_gix ON public.hazard USING gist (geometry);
