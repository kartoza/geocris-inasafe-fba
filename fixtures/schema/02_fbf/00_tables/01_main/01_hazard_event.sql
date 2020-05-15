--
-- Name: hazard_event; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS public.hazard_event (
    id integer NOT NULL,
    hazard_map_id integer,
    acquisition_date timestamp without time zone DEFAULT now() NOT NULL,
    forecast_date timestamp without time zone,
    source text,
    notes text,
    link text,
    trigger_status integer,
    progress integer,
    hazard_type_id integer,
    CONSTRAINT hazard_event_progress_fkey FOREIGN KEY (progress) REFERENCES public.progress_status(id),
    CONSTRAINT hazard_event_trigger_status_fkey FOREIGN KEY (trigger_status) REFERENCES public.trigger_status(id),
    CONSTRAINT forecast_hazard_event_hazard_map_id_fkey FOREIGN KEY (hazard_map_id) REFERENCES public.hazard_map(id),
    CONSTRAINT hazard_type_fkey FOREIGN KEY (hazard_type_id) REFERENCES public.hazard_type(id),
    CONSTRAINT forecast_hazard_event_pkey PRIMARY KEY (id)
);


--
-- Name: forecast_hazard_event_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE IF NOT EXISTS public.forecast_hazard_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: forecast_hazard_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.forecast_hazard_event_id_seq OWNED BY public.hazard_event.id;

--
-- Name: hazard_event id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hazard_event ALTER COLUMN id SET DEFAULT nextval('public.forecast_hazard_event_id_seq'::regclass);

--
-- Name: hazard_event_idx_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX IF NOT EXISTS hazard_event_idx_id ON public.hazard_event USING btree (id);


--
-- Name: hazard_event_idx_map_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX IF NOT EXISTS hazard_event_idx_map_id ON public.hazard_event USING btree (hazard_map_id);
