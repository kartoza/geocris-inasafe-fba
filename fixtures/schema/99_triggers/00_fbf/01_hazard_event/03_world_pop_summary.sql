DROP TRIGGER IF EXISTS hazard_event_tg_00_exposed_world_pop_mv ON public.hazard_event;
CREATE TRIGGER hazard_event_tg_00_exposed_world_pop_mv AFTER INSERT ON public.hazard_event FOR EACH STATEMENT EXECUTE PROCEDURE public.kartoza_refresh_hazard_event_world_pop_mv();
