import json
from collections import OrderedDict
from datetime import datetime, timedelta

import requests
from dateutil.parser import isoparse
from glofas.layer.reporting_point import (
    ReportingPointAPI,
    ReportingPointResult)
from osgeo import ogr


class GloFASForecast(object):

    TRIGGER_STATUS_NO_ACTIVATION = 0
    TRIGGER_STATUS_PRE_ACTIVATION = 1
    TRIGGER_STATUS_ACTIVATION = 2

    PROGRESS_IN_PROGRESS = 1
    PROGRESS_DONE = 2

    _default_point_layer_source = (
        'http://78.47.62.69/geoserver/kartoza/ows?service=WFS&version=1'
        '.0.0&request=GetFeature&typeName=kartoza:reporting_point'
        '&maxFeatures=50&outputFormat=application/json&srsName=EPSG:4326')
    _default_pre_activation_lead_time = 10
    _default_activation_lead_time = 3
    _default_pre_activation_eps_min_probability = 0
    _default_activation_eps_min_probability = 0
    # Note below, we want to preserve the order.
    # Increasing alert priority order
    # Mapping is the alert level into return period range
    _default_alert_level_return_period_mapping = OrderedDict(
        [
            (ReportingPointResult.ALERT_LEVEL_MEDIUM, [2, 5]),
            (ReportingPointResult.ALERT_LEVEL_HIGH, [5, 20]),
            (ReportingPointResult.ALERT_LEVEL_SEVERE, [20, 100]),
        ])
    # Minimum alert corresponds to the index of alert_level mapping above
    _default_pre_activation_minimum_alert = 1
    _default_activation_minimum_alert = 2
    # Impact limit
    _default_pre_activation_impact_limit = 0
    _default_activation_impact_limit = 0

    # Hazard map query filter
    _default_postgrest_url = 'http://78.46.133.148:3000/'
    _default_hazard_map_query_filter = 'hazard_map?select=*,reporting_point(id,glofas_id)&reporting_point.glofas_id=eq.{station_id}&measuring_station_id=not.is.null&and=(return_period.gte.{return_period_min},return_period.lt.{return_period_max})'
    _default_plpy_query_hazard_map_filter ='select hazard_map.* from hazard_map join reporting_point on hazard_map.measuring_station_id = reporting_point.id where reporting_point.glofas_id = $1 and return_period >= $2 and return_period < $3'

    # Hazard Forecast query filter
    _default_hazard_forecast_event_query_filter = 'hazard_event?select=id,hazard_map_id,acquisition_date,forecast_date,source,notes,link,trigger_status,progress&acquisition_date=lt.{acquisition_date}&forecast_date=eq.{forecast_date}&source=eq.{source}&order=acquisition_date.desc'
    _default_plpy_hazard_forecast_event_filter = 'select id,hazard_map_id,acquisition_date,forecast_date,source,notes,link,trigger_status,progress from hazard_event where acquisition_date < $1 and forecast_date = $2 and source = $3'

    # Hazard forecast delete
    _default_hazard_event_delete_query_filter = '&and=(hazard_map_id.eq.{hazard_map_id},acquisition_date.eq.{acquisition_date},forecast_date.eq.{forecast_date},source.eq.{source})'
    _default_plpy_hazard_event_delete_filter = 'delete from hazard_event where hazard_map_id = $1 and acquisition_date = $2 and forecast_date = $3 and source = $4'

    # Hazard Forecast insert
    _default_hazard_event_insert_endpoint = 'hazard_event?select=id,hazard_map_id,acquisition_date,forecast_date,source,notes,link,trigger_status,progress'
    _default_plpy_hazard_event_insert_query = 'insert into hazard_event (hazard_map_id, acquisition_date, forecast_date, source, notes, link, trigger_status, progress) select hazard_map_id, acquisition_date, forecast_date, source, notes, link, trigger_status, progress from json_populate_recordset(null::hazard_event, $1) returning id'

    # Impact query
    _default_impacted_village_query_filter = 'vw_village_impact?hazard_event_id=eq.{hazard_event_id}&impact_ratio=gte.{impact_limit}'

    # Region trigger status query
    _default_region_trigger_status_endpoint = '{region}_trigger_status'
    _default_region_trigger_status_delete_query_param = '?hazard_event_id=eq.{hazard_event_id}'
    _default_region_trigger_status_query_filter = '{region}_trigger_status?hazard_event_id=eq.{hazard_event_id}'

    # Administrative mapping
    _default_parent_administrative_mapping = 'mv_administrative_mapping?select={parent_region}_id,{child_region}_id&{child_region}_id=in.{child_ids}'

    # Calculate impact
    _default_rpc_calculate_impact='rpc/kartoza_calculate_impact'
    _default_rpc_generate_report = 'rpc/kartoza_fba_generate_excel_report_for_hazard'

    def __init__(
            self,
            reporting_point_layer_source=None,
            pre_activation_lead_time=_default_pre_activation_lead_time,
            activation_lead_time=_default_activation_lead_time,
            pre_activation_eps_min_probability=_default_pre_activation_eps_min_probability,
            activation_eps_min_probability=_default_activation_eps_min_probability,
            alert_level_return_period_mapping=_default_alert_level_return_period_mapping,
            pre_activation_minimum_alert=_default_pre_activation_minimum_alert,
            activation_minimum_alert=_default_activation_minimum_alert,
            pre_activation_impact_limit=_default_pre_activation_impact_limit,
            activation_impact_limit=_default_activation_impact_limit,
            #  Query config
            use_plpy=False,
            postgrest_url=_default_postgrest_url,
            # Hazard Map Query
            hazard_map_query_filter=_default_hazard_map_query_filter,
            plpy_query_hazard_map_filter=_default_plpy_query_hazard_map_filter,
            # Hazard Event Query
            hazard_event_query_filter=_default_hazard_forecast_event_query_filter,
            plpy_hazard_event_filter=_default_plpy_hazard_forecast_event_filter,
            # Hazard Event Deletion
            hazard_event_delete_query_filter=_default_hazard_event_delete_query_filter,
            plpy_hazard_event_delete_filter=_default_plpy_hazard_event_delete_filter,
            # Hazard Event insertion
            hazard_event_insert_endpoint=_default_hazard_event_insert_endpoint,
            plpy_hazard_event_insert_query=_default_plpy_hazard_event_insert_query,
            # Impact limit query
            impacted_village_query_filter=_default_impacted_village_query_filter,
            # Region trigger status query
            region_trigger_status_endpoint=_default_region_trigger_status_endpoint,
            region_trigger_status_delete_query_param=_default_region_trigger_status_delete_query_param,
            region_trigger_status_query_filter=_default_region_trigger_status_query_filter,
            # Administrative mapping
            parent_administrative_mapping=_default_parent_administrative_mapping,
            # Calculate impact
            rpc_calculate_impact=_default_rpc_calculate_impact,
            rpc_generate_report=_default_rpc_generate_report):
        self.api = ReportingPointAPI()
        self.point_layer_source = (
                reporting_point_layer_source
                or GloFASForecast._default_point_layer_source)
        self.pre_activation_lead_time = pre_activation_lead_time
        self.activation_lead_time = activation_lead_time
        self.pre_activation_eps_min_probability = pre_activation_eps_min_probability
        self.activation_eps_min_probability = activation_eps_min_probability
        self.alert_level_return_period_mapping = alert_level_return_period_mapping
        self.pre_activation_minimum_alert = pre_activation_minimum_alert
        self.activation_minimum_alert = activation_minimum_alert
        self.pre_activation_impact_limit = pre_activation_impact_limit
        self.activation_impact_limit = activation_impact_limit
        ##
        self.postgrest_url = postgrest_url
        self.hazard_map_query_filter = hazard_map_query_filter
        self.use_plpy = use_plpy
        self.plpy_query_hazard_map_filter = plpy_query_hazard_map_filter
        self.hazard_event_query_filter = hazard_event_query_filter
        self.plpy_hazard_event_filter = plpy_hazard_event_filter
        self.hazard_event_insert_endpoint = hazard_event_insert_endpoint
        self.plpy_hazard_event_insert_query = plpy_hazard_event_insert_query
        self.hazard_event_delete_query_filter = hazard_event_delete_query_filter
        self.plpy_hazard_event_delete_filter = plpy_hazard_event_delete_filter
        self.impacted_village_query_filter = impacted_village_query_filter
        self.region_trigger_status_endpoint = region_trigger_status_endpoint
        self.region_trigger_status_delete_query_param = region_trigger_status_delete_query_param
        self.region_trigger_status_query_filter = region_trigger_status_query_filter
        self.parent_administrative_mapping = parent_administrative_mapping
        self.rpc_calculate_impact = rpc_calculate_impact
        self.rpc_generate_report = rpc_generate_report
        ##
        self.source_text = 'GloFAS - Reporting Point'
        self.feature_info = []
        self.hazard_forecast_events = []

    @property
    def acquisition_time(self):
        return self.api.time

    @acquisition_time.setter
    def acquisition_time(self, value):
        self.api.time = value or datetime.today().replace(
            hour=0, minute=0, second=0, microsecond=0)

    def find_hazard_map_plpy(self, station_id, return_period_min, return_period_max):
        import plpy

        plan = plpy.prepare(self.plpy_query_hazard_map_filter,
                            ["int", "int", "int"])
        result = plpy.execute(plan, [station_id, return_period_min,
                                     return_period_max])

        if len(result) == 0:
            # We didn't found any hazard map
            return None

        # We found the hazard map
        row = result[0]
        return row['id']

    def find_hazard_map_postgrest(
            self, station_id, return_period_min, return_period_max):
        query_param = self.hazard_map_query_filter.format(
            station_id=station_id,
            return_period_min=return_period_min,
            return_period_max=return_period_max
        )
        url = '{postgrest_url}/{query_param}'.format(
            postgrest_url=self.postgrest_url,
            query_param=query_param)
        response = requests.get(url)
        try:
            hazard_map_id = None
            result = response.json()
            hazard_map_id = result[0]['id']
        finally:
            return hazard_map_id

    def find_previous_hazard_forecast_postgrest(
            self, forecast_date, maximum_acquisition_date, source):
        query_param = self.hazard_event_query_filter.format(
            acquisition_date=maximum_acquisition_date,
            forecast_date=forecast_date,
            source=source)
        url = '{postgrest_url}/{query_param}'.format(
            postgrest_url=self.postgrest_url,
            query_param=query_param)
        response = requests.get(url)
        try:
            hazard_event = None
            result = response.json()
            hazard_event = result[0]
        finally:
            return hazard_event

    def find_previous_hazard_forecast_plpy(
            self, forecast_date, maximum_acquisition_date, source):
        import plpy

        plan = plpy.prepare(self.plpy_query_hazard_map_filter,
                            ["timestamp", "timestamp", "varchar"])
        result = plpy.execute(
            plan, [maximum_acquisition_date.isoformat(), forecast_date.isoformat(), source])

        if len(result) == 0:
            # We didn't found any hazard map
            return None

        # We found the hazard map
        row = result[0]
        return row

    def _evaluate_hazard_forecast_activation_candidate(
            self,
            current_hazard_forecast,
            forecast_eps,
            relative_forecast_day,
            reporting_point_result,
            acquisition_date):
        total_alert_level = len(self.alert_level_return_period_mapping.keys())
        # Determine if alert level eligible for activation
        for alert_level_index in range(total_alert_level):

            alert_level = \
                list(self.alert_level_return_period_mapping)[
                    alert_level_index]
            return_period = \
                self.alert_level_return_period_mapping[alert_level]

            if alert_level_index < \
                    self.activation_minimum_alert:
                # skip if not eligible
                continue

            # Determine if there are significant forecast_eps with
            # sufficient lead time

            # see if it passes confidence threshold/probability
            # threshold
            forecast_value = forecast_eps[alert_level]
            if forecast_value < \
                    self.activation_eps_min_probability:
                # skip if probability is less than threshold
                continue

            # We have high enough probability, so proceed
            forecast_date = acquisition_date + timedelta(
                days=relative_forecast_day)

            # Find available corresponding hazard map model from
            # database
            # Criteria is based on:
            #  - matching of return period in range
            #  - matching station id

            station_id = reporting_point_result.point_no
            return_period_min = return_period[0]
            return_period_max = return_period[1]

            if self.use_plpy:
                hazard_map_id = self.find_hazard_map_plpy(
                    station_id,
                    return_period_min,
                    return_period_max)
            else:
                hazard_map_id = self.find_hazard_map_postgrest(
                    station_id,
                    return_period_min,
                    return_period_max)

            # If we don't have hazard map, skip
            if not hazard_map_id:
                continue

            # The forecast_eps will have hazard map and
            # is eligible for activation test
            # Determine eligibility based on previous pre-activation

            # Check previous forecast activation
            if self.use_plpy:
                hazard_event = self.find_previous_hazard_forecast_plpy(
                    forecast_date,
                    acquisition_date - timedelta(days=1),
                    current_hazard_forecast['source'])
            else:
                hazard_event = self.find_previous_hazard_forecast_postgrest(
                    forecast_date,
                    acquisition_date - timedelta(days=1),
                    current_hazard_forecast['source'])

            if not hazard_event:
                # No previous forecast
                continue

            previous_trigger_status = hazard_event['trigger_status']
            if not (
                    previous_trigger_status ==
                    GloFASForecast.TRIGGER_STATUS_PRE_ACTIVATION
                    or previous_trigger_status ==
                    GloFASForecast.TRIGGER_STATUS_ACTIVATION):
                # It will not trigger activation
                # Skip
                continue

            # This hazard forecast_eps now an activation candidate
            # Because several days ago the forecast_eps has been in a
            # pre-activation trigger state
            # Define new hazard forecast_eps definition
            current_hazard_forecast = {
                'hazard_map_id': hazard_map_id,
                'acquisition_date': acquisition_date,
                'forecast_date': forecast_date,
                'source': self.source_text,
                'alert_level_key': alert_level,
                'notes': 'Alert Warning Level: {alert_level}'.format(
                    alert_level=alert_level.upper()),
                'link': 'https://globalhazards.eu/',
                'trigger_status_candidate':
                    GloFASForecast.TRIGGER_STATUS_ACTIVATION
            }
            # This means, out of this loop, current hazard forecast_eps is
            # from the highest severity available that passes
            # activation criteria
        return current_hazard_forecast

    def _evaluate_hazard_forecast_pre_activation_candidate(
            self,
            current_hazard_forecast,
            forecast_eps,
            relative_forecaste_day,
            reporting_point_result,
            acquisition_date):
        # Determine if alert level eligible for pre activation
        total_alert_level = len(self.alert_level_return_period_mapping.keys())

        contexts = []
        for alert_level_index in range(total_alert_level):

            alert_level = \
                list(self.alert_level_return_period_mapping)[
                    alert_level_index]
            return_period = \
                self.alert_level_return_period_mapping[alert_level]

            if alert_level_index < self.pre_activation_minimum_alert:
                # skip if not eligible
                contexts.append('Skip because low alert level')
                continue

            # Determine if there are significant forecast_eps with
            # sufficient lead time

            # see if it passes confidence threshold/probability threshold
            forecast_value = forecast_eps[alert_level]
            if forecast_value < \
                    self.pre_activation_eps_min_probability:
                # skip if probability is less than threshold
                contexts.append('Skip because low probability')
                continue

            # We have high enough probability, so proceed
            forecast_date = acquisition_date + timedelta(
                days=relative_forecaste_day)

            # Find available corresponding hazard map model from database
            # Criteria is based on:
            #  - matching of return period in range
            #  - matching station id

            station_id = reporting_point_result.point_no
            return_period_min = return_period[0]
            return_period_max = return_period[1]

            if self.use_plpy:
                hazard_map_id = \
                    self.find_hazard_map_plpy(
                        station_id,
                        return_period_min,
                        return_period_max)
            else:
                hazard_map_id = \
                    self.find_hazard_map_postgrest(
                        station_id,
                        return_period_min,
                        return_period_max)

            # If we don't have hazard map, skip
            if not hazard_map_id:
                contexts.append('Skip because hazard map not found')
                continue

            # If we have hazard map. Make a hazard forecast_eps candidate
            current_hazard_forecast = {
                'hazard_map_id': hazard_map_id,
                'acquisition_date': acquisition_date,
                'forecast_date': forecast_date,
                'source': self.source_text,
                'alert_level_key': alert_level,
                'notes': 'Alert Warning Level: {alert_level}'.format(
                    alert_level=alert_level.upper()),
                'link': 'https://globalhazards.eu/',
                'trigger_status_candidate':
                    GloFASForecast.TRIGGER_STATUS_PRE_ACTIVATION,
            }
            # The forecast_eps is eligible for pre-activation
            # This means, out of this loop, current hazard forecast_eps is
            # from the highest severity available that passes
            # pre-activation criteria

        return current_hazard_forecast

    def push_hazard_forecast_event_postgrest(self, hazard_forecast_events):
        url = '{postgrest_url}/{query_param}'.format(
            postgrest_url=self.postgrest_url,
            query_param=self.hazard_event_insert_endpoint)
        headers = {
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
        # Filter only the needed column
        hazard_events = [
            {
                'hazard_map_id': v['hazard_map_id'],
                'acquisition_date': v['acquisition_date'].isoformat(),
                'forecast_date': v['forecast_date'].isoformat(),
                'source': v['source'],
                'notes': v['notes'],
                'link': v['link'],
                'trigger_status': v['trigger_status_candidate'],
                # Progress 1 means, impact level has not been calculated
                'progress': GloFASForecast.PROGRESS_IN_PROGRESS
            }
            for v in hazard_forecast_events
        ]
        json_string = json.dumps(hazard_events)

        # The process needs to be idempotent, so delete matching forecast first
        query_param = self.hazard_event_delete_query_filter
        for event in hazard_events:
            delete_url = url + query_param.format(**event)
            requests.delete(delete_url)

        # Bulk inserts
        response = requests.post(
            url,
            data=json_string,
            headers=headers)
        # Get the returned ids
        created = response.json()
        return [c['id'] for c in created]

    def push_hazard_forecast_event_plpy(self, hazard_forecast_events):
        import plpy

        # Filter only the needed column
        hazard_events = [
            {
                'hazard_map_id': v['hazard_map_id'],
                'acquisition_date': v['acquisition_date'].isoformat(),
                'forecast_date': v['forecast_date'].isoformat(),
                'source': v['source'],
                'notes': v['notes'],
                'link': v['link'],
                'trigger_status': v['trigger_status_candidate'],
                # Progress 1 means, impact level has not been calculated
                'progress': GloFASForecast.PROGRESS_IN_PROGRESS
            }
            for v in hazard_forecast_events
        ]
        json_string = json.dumps(hazard_events)

        # The process needs to be idempotent, so delete matching forecast first
        for event in hazard_events:
            plan = plpy.prepare(
                self.plpy_hazard_event_delete_filter,
                ["int", "timestamp", "timestamp", "varchar"])
            plpy.execute(plan,[
                event['hazard_map_id'],
                event['acquisition_date'],
                event['forecast_date'],
                event['source']
            ])

        # We bulk insert the events
        plan = plpy.prepare(
            self.plpy_hazard_event_insert_query, ["text"])
        result = plpy.execute(plan, [json_string])
        return result

    def fetch_forecast(self, acquisition_date=None):
        # Fetch forecast from GloFAS
        # Get point layer
        ds = ogr.Open(self.point_layer_source)
        point_layer = ds.GetLayer()
        # Get the forecast itself
        self.acquisition_time = acquisition_date or self.acquisition_time
        self.feature_info = self.api.get_feature_info(point_layer, srs='EPSG:4326')

    def process_forecast(self):
        # determine current date
        today = self.acquisition_time

        hazard_forecast_events = []

        # iterate thru all reporting points
        for info in self.feature_info:

            # Combine alert level and forecasted EPS values so we can iterate
            # for each date
            forecast_days = []
            for key, value in self.alert_level_return_period_mapping.items():
                eps_array = info.eps_array(key)
                for i in range(len(eps_array)):
                    eps = eps_array[i]
                    try:
                        forecast = forecast_days[i]
                    except:
                        forecast = {}

                    forecast[key] = eps
                    try:
                        forecast_days[i] = forecast
                    except:
                        forecast_days.append(forecast)

            # Iterate each date
            for i in range(len(forecast_days)):

                if forecast_days[i]['medium'] == 0:
                    continue

                # Get the forecast
                forecast = forecast_days[i]
                current_hazard_forecast = {}

                # Evaluate pre activation condition
                current_hazard_forecast = \
                    self._evaluate_hazard_forecast_pre_activation_candidate(
                        current_hazard_forecast, forecast, i, info, today)

                # If we don't have pre-activation candidate, skip to next day
                if not current_hazard_forecast:
                    continue

                # Activation evaluation should be considered if the event
                # is a pre-activation candidate
                # Other than that, we don't have to evaluate it.
                # Now evaluate activation condition
                current_hazard_forecast = \
                    self._evaluate_hazard_forecast_activation_candidate(
                        current_hazard_forecast, forecast, i, info, today)

                # current forecast now is best guess/candidate
                # of hazard forecast
                if current_hazard_forecast:
                    hazard_forecast_events.append(current_hazard_forecast)

        # We now have hazard forecast event candidate
        # We push it to DB so the impact level can be calculated
        if self.use_plpy:
            created_ids = self.push_hazard_forecast_event_plpy(hazard_forecast_events)
        else:
            created_ids = self.push_hazard_forecast_event_postgrest(hazard_forecast_events)

        # patch id into the objects
        for i in range(len(hazard_forecast_events)):
            hazard_event_id = created_ids[i]
            hazard_event = hazard_forecast_events[i]
            hazard_event['id'] = hazard_event_id

        # store candidates data
        self.hazard_forecast_events = hazard_forecast_events

    def fetch_impacted_village(self, hazard_event_id, impact_limit):
        query_param = self.impacted_village_query_filter.format(
            hazard_event_id=hazard_event_id,
            impact_limit=impact_limit)
        url = '{postgrest_url}/{query_param}'.format(
            postgrest_url=self.postgrest_url,
            query_param=query_param)
        response = requests.get(url)
        return response.json()

    def find_region_trigger_status(self, region, hazard_event_id):
        query_param = self.region_trigger_status_query_filter.format(
            region=region,
            hazard_event_id=hazard_event_id)
        url = '{postgrest_url}/{query_param}'.format(
            postgrest_url=self.postgrest_url,
            query_param=query_param)
        response = requests.get(url)
        return response.json()

    def find_village_trigger_status(self, hazard_event_id):
        return self.find_region_trigger_status('village', hazard_event_id)

    def find_sub_district_trigger_status(self, hazard_event_id):
        return self.find_region_trigger_status('sub_district', hazard_event_id)

    def find_district_trigger_status(self, hazard_event_id):
        return self.find_region_trigger_status('district', hazard_event_id)

    def push_region_trigger_status(self, region, trigger_status_array):
        endpoint = self.region_trigger_status_endpoint.format(
            region=region)
        url = '{postgrest_url}/{endpoint}'.format(
            postgrest_url=self.postgrest_url,
            endpoint=endpoint)

        # The process needs to be idempotent
        # So delete existing status first
        query_param = self.region_trigger_status_delete_query_param
        if not trigger_status_array:
            return
        hazard_event_id = trigger_status_array[0]['hazard_event_id']
        delete_url = url + query_param.format(hazard_event_id=hazard_event_id)
        requests.delete(delete_url)

        headers = {
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
        # Bulk inserts
        json_string = json.dumps(trigger_status_array)
        response = requests.post(
            url,
            data=json_string,
            headers=headers)
        # Get the returned ids
        return response.json()

    def push_village_trigger_status(self, trigger_status_array):
        return self.push_region_trigger_status('village', trigger_status_array)

    def push_sub_district_trigger_status(self, trigger_status_array):
        return self.push_region_trigger_status('sub_district', trigger_status_array)

    def push_district_trigger_status(self, trigger_status_array):
        return self.push_region_trigger_status('district', trigger_status_array)

    def fetch_parent_administrative_mapping(self, parent_region, child_region, child_ids):
        json_array = '({})'.format(','.join([str(c) for c in child_ids]))
        query_param = self.parent_administrative_mapping.format(
            parent_region=parent_region,
            child_region=child_region,
            child_ids=json_array)
        url = '{postgrest_url}/{query_param}'.format(
            postgrest_url=self.postgrest_url,
            query_param=query_param)
        response = requests.get(url)
        mapping = response.json()

        # reverse the mapping as hash
        admin_hash = {}
        for m in mapping:
            child_id = m['{}_id'.format(child_region)]
            parent_id = m['{}_id'.format(parent_region)]
            admin_hash[child_id] = parent_id
        return admin_hash

    def fetch_sub_district_mapping(self, child_ids):
        return self.fetch_parent_administrative_mapping('sub_district', 'village', child_ids)

    def fetch_district_mapping(self, child_ids):
        return self.fetch_parent_administrative_mapping('district', 'sub_district', child_ids)

    def update_hazard_event_forecast(self, hazard_event):
        url = '{postgrest_url}/{query_param}'.format(
            postgrest_url=self.postgrest_url,
            query_param=self.hazard_event_insert_endpoint)
        headers = {
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
        # Filter only the needed column to patch
        patch_data = {
            'trigger_status': hazard_event['trigger_status'],
            'progress': hazard_event['progress']
        }
        json_string = json.dumps(patch_data)

        # Perform update
        response = requests.patch(
            url + '&id=eq.{id}'.format(id=hazard_event['id']),
            data=json_string,
            headers=headers)
        # Get the returned ids
        updated = response.json()

        return updated

    def evaluate_trigger_status(self, forecast_events=None):
        self.hazard_forecast_events = (
            forecast_events or self.hazard_forecast_events)

        # Evaluate trigger status by considering impact level
        # At this point, impact data should already been calculated in the DB
        for hazard_forecast in self.hazard_forecast_events:

            # Evaluate pre activation criteria
            # Find impact data:
            villages_data = self.fetch_impacted_village(
                hazard_forecast['id'], self.pre_activation_impact_limit)
            # Update each municipality trigger status
            # All villages that exceed impact limit means it is a
            # pre activation candidate

            if not villages_data:
                # Skip if impact tolerated
                hazard_forecast['trigger_status'] = GloFASForecast.TRIGGER_STATUS_NO_ACTIVATION
                hazard_forecast['progress'] = GloFASForecast.PROGRESS_DONE

                # Update hazard_forecast information
                self.update_hazard_event_forecast(hazard_forecast)
                continue

            # Create village trigger status mapping
            village_trigger_status = [
                {
                    'hazard_event_id': hazard_forecast['id'],
                    'village_id': v['village_id'],
                    'trigger_status': GloFASForecast.TRIGGER_STATUS_PRE_ACTIVATION
                } for v in villages_data
            ]

            # Evaluate activation criteria
            # Check previous forecast activation
            forecast_date = hazard_forecast['forecast_date']
            today = hazard_forecast['acquisition_date']
            if isinstance(today, str):
                today = isoparse(today)

            acquisition_date = today - timedelta(days=1)
            if self.use_plpy:
                hazard_event = self.find_previous_hazard_forecast_plpy(
                    forecast_date,
                    acquisition_date,
                    hazard_forecast['source'])
            else:
                hazard_event = self.find_previous_hazard_forecast_postgrest(
                    forecast_date,
                    acquisition_date,
                    hazard_forecast['source'])

            if hazard_event:
                # We have previous forecast
                # Check if previous forecast is in pre activation stage
                previous_village_trigger_status = self.find_village_trigger_status(
                    hazard_event['id'])
                # Create hash
                prev_village_hash = {}
                for village_state in previous_village_trigger_status:
                    status = village_state['trigger_status']
                    if status == GloFASForecast.TRIGGER_STATUS_PRE_ACTIVATION or status == GloFASForecast.TRIGGER_STATUS_ACTIVATION:
                        prev_village_hash[village_state['village_id']] =  village_state['trigger_status']

                # Evaluate which village exceed activation impact limit
                activation_candidate_village_data = self.fetch_impacted_village(
                    hazard_forecast['id'], self.activation_impact_limit)

                activation_candidate_village_data = [v['village_id'] for v in activation_candidate_village_data]

                # Update trigger_status
                for village_state in village_trigger_status:
                    village_id = village_state['village_id']
                    # If it satisfy activation criteria, activate
                    if village_id in prev_village_hash and village_id in activation_candidate_village_data:
                        village_state['trigger_status'] = GloFASForecast.TRIGGER_STATUS_ACTIVATION

            # Insert to DB
            self.push_village_trigger_status(village_trigger_status)
            # Determine sub districts status
            sub_district_hash = {}
            # Fetch sub district mapping
            village_ids = [v['village_id'] for v in village_trigger_status]
            sub_district_mapping = self.fetch_sub_district_mapping(village_ids)

            for village_state in village_trigger_status:
                sub_district = sub_district_mapping[village_state['village_id']]
                status = village_state['trigger_status']
                try:
                    sub_district_hash[sub_district] = status if status > sub_district_hash[sub_district] else sub_district_hash[sub_district]
                except KeyError:
                    sub_district_hash[sub_district] = status

            # Reformat to array
            sub_district_trigger_status = []
            for key, value in sub_district_hash.items():
                sub_district_trigger_status.append({
                    'sub_district_id': key,
                    'hazard_event_id': hazard_forecast['id'],
                    'trigger_status': value
                })
            self.push_sub_district_trigger_status(sub_district_trigger_status)

            # Determine district status
            district_hash = {}
            # Fetch district mapping
            sub_district_ids = [s['sub_district_id'] for s in sub_district_trigger_status]
            district_mapping = self.fetch_district_mapping(sub_district_ids)

            for sub_district_state in sub_district_trigger_status:
                district = district_mapping[sub_district_state['sub_district_id']]
                status = sub_district_state['trigger_status']
                try:
                    district_hash[district] = status if status > district_hash[district] else district_hash[district]
                except KeyError:
                    district_hash[district] = status

            # Reformat to array
            district_trigger_status = []
            for key, value in district_hash.items():
                district_trigger_status.append({
                    'district_id': key,
                    'hazard_event_id': hazard_forecast['id'],
                    'trigger_status': value
                })
            self.push_district_trigger_status(district_trigger_status)

            # Update trigger status of the forecast
            final_trigger_status = GloFASForecast.TRIGGER_STATUS_PRE_ACTIVATION
            for district_state in district_trigger_status:
                status = district_state['trigger_status']
                final_trigger_status = status if status > final_trigger_status else final_trigger_status

            hazard_forecast['trigger_status'] = final_trigger_status
            hazard_forecast['progress'] = GloFASForecast.PROGRESS_DONE

            # Update hazard_forecast information
            self.update_hazard_event_forecast(hazard_forecast)

    def calculate_impact(self):
        # We calculate impact by triggering database functions.
        # Calculations happens in database
        url = '{postgrest_url}/{query_param}'.format(
            postgrest_url=self.postgrest_url,
            query_param=self.rpc_calculate_impact)
        response = requests.post(url)
        return response.status_code == 200

    def generate_report(self):
        # We generate report by triggering database functions.

        url = '{postgrest_url}/{query_param}'.format(
            postgrest_url=self.postgrest_url,
            query_param=self.rpc_generate_report)
        for f in self.hazard_forecast_events:
            data = {
                'hazard_event_id': f['id']
            }
            requests.post(url, json=data)
        return True

    def run(self, generate_report=True):
        self.fetch_forecast()
        self.process_forecast()
        self.calculate_impact()
        self.evaluate_trigger_status()
        self.calculate_impact()
        if generate_report:
            self.generate_report()


if __name__ == '__main__':
    job = GloFASForecast()
    job.run()
