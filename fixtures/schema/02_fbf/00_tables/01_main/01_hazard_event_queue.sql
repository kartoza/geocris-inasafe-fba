CREATE TABLE IF NOT EXISTS public.hazard_event_queue (
    id bigint NOT NULL,
    hazard_map_id integer,
    acquisition_date timestamp without time zone DEFAULT now() NOT NULL,
    forecast_date timestamp without time zone,
    source text,
    notes text,
    link text,
    trigger_status integer,
    progress integer,
    hazard_type_id integer,
    queue_status integer
);

CREATE SEQUENCE IF NOT EXISTS public.hazard_event_queue_seq as bigint;

ALTER SEQUENCE public.hazard_event_queue_seq OWNED BY public.hazard_event_queue.id;

ALTER TABLE ONLY public.hazard_event_queue ALTER COLUMN id SET DEFAULT nextval('public.hazard_event_queue_seq'::regclass);
