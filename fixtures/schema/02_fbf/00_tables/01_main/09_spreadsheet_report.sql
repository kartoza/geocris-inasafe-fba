--
-- Name: spreadsheet_reports; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS public.spreadsheet_reports (
    id integer NOT NULL,
    hazard_event_id integer,
    spreadsheet bytea,
    CONSTRAINT spreadsheet_reports_pkey PRIMARY KEY (id),
    CONSTRAINT spreadsheet_reports_hazard_event_id_fkey FOREIGN KEY (hazard_event_id) REFERENCES public.hazard_event(id)
);


--
-- Name: spreadsheet_reports_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE IF NOT EXISTS public.spreadsheet_reports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: spreadsheet_reports_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.spreadsheet_reports_id_seq OWNED BY public.spreadsheet_reports.id;




--
-- Name: spreadsheet_reports id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.spreadsheet_reports ALTER COLUMN id SET DEFAULT nextval('public.spreadsheet_reports_id_seq'::regclass);

