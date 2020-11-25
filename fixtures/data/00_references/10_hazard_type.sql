INSERT INTO public.hazard_type (id, name) VALUES (1, 'Flood') ON CONFLICT DO NOTHING ;
INSERT INTO public.hazard_type (id, name) VALUES (2, 'Hurricane') ON CONFLICT DO NOTHING ;
INSERT INTO public.hazard_type (id, name) VALUES (3, 'Hurricane NOAA') ON CONFLICT DO NOTHING ;
