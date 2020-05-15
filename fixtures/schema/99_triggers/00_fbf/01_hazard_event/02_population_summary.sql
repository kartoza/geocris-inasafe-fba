--
-- Name: hazard_event hazard_event_roads_mv_tg; Type: TRIGGER; Schema: public; Owner: -
--
DROP TRIGGER IF EXISTS hazard_event_tg_00_exposed_population_mv ON public.hazard_event;
CREATE TRIGGER hazard_event_tg_00_exposed_population_mv AFTER INSERT ON public.hazard_event FOR EACH STATEMENT EXECUTE PROCEDURE public.kartoza_refresh_hazard_event_population_mv();
