--
-- Name: hazard_event hazard_event_tg_00_exposed_buildings_mv; Type: TRIGGER; Schema: public; Owner: -
--
DROP TRIGGER IF EXISTS hazard_event_tg_00_exposed_buildings_mv ON public.hazard_event;
CREATE TRIGGER hazard_event_tg_00_exposed_buildings_mv AFTER INSERT ON public.hazard_event FOR EACH STATEMENT EXECUTE PROCEDURE public.kartoza_refresh_hazard_event_buildings_mv();
