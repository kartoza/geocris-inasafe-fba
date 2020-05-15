--
-- Name: spreadsheet_reports hazard_report_tg; Type: TRIGGER; Schema: public; Owner: -
--
-- DROP TRIGGER IF EXISTS  hazard_report_tg ON public.spreadsheet_reports;
-- CREATE TRIGGER hazard_report_tg BEFORE INSERT ON public.spreadsheet_reports FOR EACH ROW EXECUTE PROCEDURE public.kartoza_generate_excel_report_for_hazard();

