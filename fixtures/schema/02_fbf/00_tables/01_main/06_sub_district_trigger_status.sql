--
-- Name: sub_district_trigger_status; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS public.sub_district_trigger_status (
    id integer NOT NULL,
    sub_district_id double precision,
    trigger_status integer,
    hazard_event_id integer,
    CONSTRAINT sub_district_trigger_status_pkey PRIMARY KEY (id),
    CONSTRAINT sub_district_trigger_status_trigger_status_fkey FOREIGN KEY (trigger_status) REFERENCES public.trigger_status(id)
);


--
-- Name: sub_district_trigger_status_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE IF NOT EXISTS public.sub_district_trigger_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sub_district_trigger_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sub_district_trigger_status_id_seq OWNED BY public.sub_district_trigger_status.id;


--
-- Name: sub_district_trigger_status id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sub_district_trigger_status ALTER COLUMN id SET DEFAULT nextval('public.sub_district_trigger_status_id_seq'::regclass);
