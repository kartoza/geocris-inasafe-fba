-- Register function
DROP FUNCTION IF EXISTS public.kartoza_fba_forecast_glofas;
CREATE OR REPLACE FUNCTION public.kartoza_fba_forecast_glofas() RETURNS CHARACTER VARYING
    LANGUAGE plpython3u
as
$$
from fbf.forecast.glofas.reporting_point import GloFASForecast
import json
rv = plpy.execute("SELECT value FROM config WHERE key = 'POSTGREST_BASE_URL'")
postgrest_url = json.loads(rv[0]['value'])
rv = plpy.execute("SELECT value FROM config WHERE key = 'GEOSERVER_BASE_URL'")
reporting_point_source = json.loads(rv[0]['value'])
reporting_point_source += (
    '/kartoza/ows?service=WFS&version=1'
    '.0.0&request=GetFeature&typeName=kartoza:reporting_point'
    '&maxFeatures=50&outputFormat=application/json&srsName=EPSG:4326')
job = GloFASForecast(
    reporting_point_layer_source=reporting_point_source,
    postgrest_url=postgrest_url)
job.run()

return 'OK'
$$;

CREATE OR REPLACE FUNCTION public.kartoza_fba_forecast_glofas(hazard_event_id bigint) RETURNS CHARACTER VARYING
    LANGUAGE plpython3u
as
$$
from fbf.forecast.glofas.reporting_point import GloFASForecast
import requests
import json
rv = plpy.execute("SELECT value FROM config WHERE key = 'POSTGREST_BASE_URL'")
postgrest_url = json.loads(rv[0]['value'])
rv = plpy.execute("SELECT value FROM config WHERE key = 'GEOSERVER_BASE_URL'")
reporting_point_source = json.loads(rv[0]['value'])
reporting_point_source += (
    '/kartoza/ows?service=WFS&version=1'
    '.0.0&request=GetFeature&typeName=kartoza:reporting_point'
    '&maxFeatures=50&outputFormat=application/json&srsName=EPSG:4326')
job = GloFASForecast(
    reporting_point_layer_source=reporting_point_source,
    postgrest_url=postgrest_url)

url = '{postgrest_url}{endpoint}{query_param}'.format(
    postgrest_url=postgrest_url,
    endpoint=job.hazard_event_insert_endpoint,
    query_param='&id=eq.{id}'.format(id=hazard_event_id))

response = requests.get(url)
job.hazard_forecast_events = response.json()
job.evaluate_trigger_status(job.hazard_forecast_events)
job.calculate_impact()

return 'OK'
$$;

CREATE OR REPLACE FUNCTION public.kartoza_fba_forecast_glofas(acquisition_date date) RETURNS CHARACTER VARYING
language plpython3u
as
$$
from fbf.forecast.glofas.reporting_point import GloFASForecast
import json
rv = plpy.execute("SELECT value FROM config WHERE key = 'POSTGREST_BASE_URL'")
postgrest_url = json.loads(rv[0]['value'])
rv = plpy.execute("SELECT value FROM config WHERE key = 'GEOSERVER_BASE_URL'")
reporting_point_source = json.loads(rv[0]['value'])
reporting_point_source += (
    '/kartoza/ows?service=WFS&version=1'
    '.0.0&request=GetFeature&typeName=kartoza:reporting_point'
    '&maxFeatures=50&outputFormat=application/json&srsName=EPSG:4326')
job = GloFASForecast(
    reporting_point_layer_source=reporting_point_source,
    postgrest_url=postgrest_url)
job.acquisition_time = acquisition_date
job.run()
return 'OK'
$$;

CREATE OR REPLACE FUNCTION public.kartoza_fba_forecast_glofas_update_trigger_status(hazard_event_id bigint) RETURNS CHARACTER VARYING
language plpython3u
as
$$
from fbf.forecast.glofas.reporting_point import GloFASForecast
import json
import requests

rv = plpy.execute("SELECT value FROM config WHERE key = 'POSTGREST_BASE_URL'")
postgrest_url = json.loads(rv[0]['value'])
rv = plpy.execute("SELECT value FROM config WHERE key = 'GEOSERVER_BASE_URL'")
reporting_point_source = json.loads(rv[0]['value'])
reporting_point_source += (
    '/kartoza/ows?service=WFS&version=1'
    '.0.0&request=GetFeature&typeName=kartoza:reporting_point'
    '&maxFeatures=50&outputFormat=application/json&srsName=EPSG:4326')
job = GloFASForecast(
    reporting_point_layer_source=reporting_point_source,
    postgrest_url=postgrest_url)
url = '{postgrest_url}/hazard_event?id=eq.{hazard_event_id}'.format(
    postgrest_url=postgrest_url,
    hazard_event_id=hazard_event_id)
response = requests.get(url)
job.hazard_forecast_events = response.json()
# Impact needs to be calculated twice to consider before and after trigger status
job.calculate_impact()
job.evaluate_trigger_status()
job.calculate_impact()
job.generate_report()

return 'OK'
$$;

-- Include in cron
INSERT INTO cron.job (schedule, command, nodename, username)
SELECT
    '0 * * * *', $$ select kartoza_fba_forecast_glofas() $$, '', 'postgres'
WHERE
      NOT EXISTS (
          SELECT schedule, command, nodename, username FROM cron.job
          WHERE schedule = '0 * * * *' AND command = $$ select kartoza_fba_forecast_glofas() $$ AND nodename = '' AND username = 'postgres')

