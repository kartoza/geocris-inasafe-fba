--
-- Name: hazard_map; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS public.hazard_map (
    id integer NOT NULL,
    notes character varying(255),
    measuring_station_id integer,
    place_name character varying(255),
    return_period integer,
    CONSTRAINT hazard_map_pkey PRIMARY KEY (id),
    CONSTRAINT hazard_map_reporting_point_id_fk FOREIGN KEY (measuring_station_id) REFERENCES public.reporting_point(id)
);


--
-- Name: hazard_map_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE IF NOT EXISTS public.hazard_map_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hazard_map_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.hazard_map_id_seq OWNED BY public.hazard_map.id;

--
-- Name: hazard_map id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hazard_map ALTER COLUMN id SET DEFAULT nextval('public.hazard_map_id_seq'::regclass);


--
-- Name: hazard_map_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX IF NOT EXISTS hazard_map_id ON public.hazard_map USING btree (id);

