import datetime
import json
import os
import unittest

import requests
from glofas.layer.reporting_point import ReportingPointAPI, \
    ReportingPointResult

from fbf.forecast.glofas.reporting_point import GloFASForecast


class TestGloFASForecast(unittest.TestCase):

    def setUp(self):
        self.target_postgrest = os.environ.get('POSTGREST_BASE_URL')
        self.job = GloFASForecast(
            postgrest_url=self.target_postgrest)

    def test_forecast_run(self):
        self.job.acquisition_time = datetime.datetime(
            year=2019, month=12, day=1, hour=0, minute=0, second=0)
        self.job.source_text = '[TEST] GloFAS - Reporting Point'
        self.job.run()

        hazard_event = self.job.hazard_forecast_events[0]
        hazard_id = hazard_event['id']
        self.assertEqual(
            hazard_event['alert_level_key'],
            ReportingPointResult.ALERT_LEVEL_SEVERE)
        # fetch districts summaries
        url = '{postgrest_url}/mv_hazard_event_district_summary?hazard_event_id' \
              '=eq.{id}&order=trigger_status.desc,' \
              'total_vulnerability_score.desc'.format(
            postgrest_url=self.job.postgrest_url,
            id=hazard_id
        )
        response = requests.get(url)
        district_summaries = response.json()
        self.assertEqual(len(district_summaries), 3)
        district_summary = district_summaries[2]
        self.assertEqual(district_summary['name'], 'Bogor')
        self.assertEqual(district_summary['hazarded_building_count'], 371)
        self.assertEqual(district_summary['building_count'], 5156)
        self.assertAlmostEqual(
            district_summary['total_vulnerability_score'], 211.2, 2)
        self.assertEqual(district_summary['trigger_status'], 1)
        # fetch sub districts summaries
        url = '{postgrest_url}/mv_hazard_event_sub_district_summary?' \
              'hazard_event_id=eq.{id}&order=trigger_status.desc,' \
              'total_vulnerability_score.desc'.format(
            postgrest_url=self.job.postgrest_url,
            id=hazard_id)
        response = requests.get(url)
        sub_district_summaries = response.json()
        self.assertEqual(len(sub_district_summaries), 6)
        # filter by previous district
        sub_district_summaries = [
            s for s in sub_district_summaries
            if s['district_id'] == district_summary['district_id']]
        self.assertEqual(len(sub_district_summaries), 2)
        sub_district_summary = sub_district_summaries[1]
        self.assertEqual(sub_district_summary['name'], 'Rumpin')
        self.assertEqual(
            sub_district_summary['hazarded_building_count'], 150)
        self.assertEqual(sub_district_summary['building_count'], 2198)
        self.assertAlmostEqual(
            sub_district_summary['total_vulnerability_score'], 85.6, 2)
        self.assertEqual(sub_district_summary['trigger_status'], 1)
        # fetch village summaries
        url = '{postgrest_url}/mv_hazard_event_village_summary?' \
              'hazard_event_id=eq.{id}&order=trigger_status.desc,' \
              'total_vulnerability_score.desc'.format(
            postgrest_url=self.job.postgrest_url,
            id=hazard_id)
        response = requests.get(url)
        village_summaries = response.json()
        self.assertEqual(len(village_summaries), 14)
        # filter by previous district
        village_summaries = [
            s for s in village_summaries
            if
            s['sub_district_id'] == sub_district_summary['sub_district_id']]
        self.assertEqual(len(village_summaries), 1)
        village_summary = village_summaries[0]
        self.assertEqual(village_summary['name'], 'Sukamulya')
        self.assertEqual(
            village_summary['hazarded_building_count'], 150)
        self.assertEqual(village_summary['building_count'], 2198)
        self.assertAlmostEqual(
            village_summary['total_vulnerability_score'], 85.6, 2)
        self.assertEqual(village_summary['trigger_status'], 1)

        # test download the spreadsheet
        data = {
            'hazard_event_id': hazard_id
        }
        url = '{postgrest_url}/rpc/hazard_event_spreadsheet'.format(
            postgrest_url=self.job.postgrest_url)
        response = requests.post(url, json=data)
        result = response.json()
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0]['spreadsheet_content'])

    def test_activation_criteria(self):

        self.job.acquisition_time = datetime.datetime(
            year=2019, month=12, day=19, hour=0, minute=0, second=0)
        self.job.source_text = '[TEST] GloFAS - Reporting Point'
        self.job.run(generate_report=False)

        self.job.acquisition_time = datetime.datetime(
            year=2019, month=12, day=22, hour=0, minute=0, second=0)
        self.job.run(generate_report=False)

        # validate activation result
        hazard_event = self.job.hazard_forecast_events[1]
        self.assertEqual(
            hazard_event['trigger_status'],
            GloFASForecast.TRIGGER_STATUS_ACTIVATION)

        # fetch districts summaries
        url = '{postgrest_url}/mv_hazard_event_district_summary?hazard_event_id' \
              '=eq.{id}&order=trigger_status.desc,' \
              'total_vulnerability_score.desc'.format(
            postgrest_url=self.job.postgrest_url,
            id=hazard_event['id']
        )
        response = requests.get(url)
        district_summaries = response.json()
        trigger_statuses = [d['trigger_status'] for d in district_summaries]

        self.assertIn(
            GloFASForecast.TRIGGER_STATUS_ACTIVATION,
            trigger_statuses)

        self.job.hazard_forecast_events = self.find_test_events(
            self.job.source_text)

    def find_test_events(self, source_text):
        url = '{postgrest_url}/hazard_event?source=eq.{source_text}'.format(
            postgrest_url=self.job.postgrest_url,
            source_text=source_text
        )
        response = requests.get(url)
        return response.json()

    def delete_trigger_status(self, forecast_event_ids):
        table_names = [
            'village_trigger_status',
            'sub_district_trigger_status',
            'district_trigger_status'
        ]
        for t in table_names:
            url = '{postgrest_url}/{table_name}?hazard_event_id=in.({event_ids})'.format(
                postgrest_url=self.job.postgrest_url,
                table_name=t,
                event_ids=','.join([str(i) for i in forecast_event_ids])
            )
            requests.delete(url)

    def delete_spreadsheets(self, forecast_event_ids):
        url = '{postgrest_url}/spreadsheet_reports?hazard_event_id=in.({event_ids})'.format(
            postgrest_url=self.job.postgrest_url,
            event_ids=','.join([str(i) for i in forecast_event_ids])
        )
        requests.delete(url)

    def delete_hazard_event(self, forecast_event_ids):
        url = '{postgrest_url}/hazard_event?id=in.({event_ids})'.format(
            postgrest_url=self.job.postgrest_url,
            event_ids=','.join([str(i) for i in forecast_event_ids])
        )
        requests.delete(url)

    def tearDown(self):
        # Remove testing related data
        # Get all forecast events

        event_ids = [f['id'] for f in self.job.hazard_forecast_events]
        self.delete_trigger_status(event_ids)
        self.delete_spreadsheets(event_ids)
        self.delete_hazard_event(event_ids)

