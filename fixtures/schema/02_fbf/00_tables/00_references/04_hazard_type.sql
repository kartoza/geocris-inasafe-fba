--
-- Name: hazard_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS public.hazard_type (
    id integer NOT NULL,
    name text,
    CONSTRAINT hazard_type_pkey PRIMARY KEY (id)
);


--
-- Name: hazard_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE IF NOT EXISTS public.hazard_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hazard_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.hazard_type_id_seq OWNED BY public.hazard_type.id;

--
-- Name: hazard_type id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hazard_type ALTER COLUMN id SET DEFAULT nextval('public.hazard_type_id_seq'::regclass);


