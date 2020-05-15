--
-- Name: district_trigger_status; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS public.district_trigger_status (
    id integer NOT NULL,
    district_id double precision,
    trigger_status integer,
    hazard_event_id integer,
    CONSTRAINT district_trigger_status_trigger_status_fkey
        FOREIGN KEY (trigger_status) REFERENCES public.trigger_status(id)
);


--
-- Name: district_trigger_status_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE IF NOT EXISTS public.district_trigger_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: district_trigger_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.district_trigger_status_id_seq OWNED BY public.district_trigger_status.id;
--
-- Name: district_trigger_status id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.district_trigger_status ALTER COLUMN id SET DEFAULT nextval('public.district_trigger_status_id_seq'::regclass);



