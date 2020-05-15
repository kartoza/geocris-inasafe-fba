INSERT INTO public.hazard_class (id, label, hazard_type) VALUES (1, '0 - 0.7m', 1) ON CONFLICT DO NOTHING ;
INSERT INTO public.hazard_class (id, label, hazard_type) VALUES (2, '0.7 - 1.5m', 1) ON CONFLICT DO NOTHING ;
INSERT INTO public.hazard_class (id, label, hazard_type) VALUES (3, '1.5 - 3.0m', 1) ON CONFLICT DO NOTHING ;
INSERT INTO public.hazard_class (id, label, hazard_type) VALUES (4, '3 or greater', 1) ON CONFLICT DO NOTHING ;
