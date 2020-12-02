import requests
from unittest import mock

from django.core.management import call_command
from django.test import TestCase


original_requests_get = requests.get


def mock_get_geocris_noaa_api(url, *args, **kwargs):
    if url.endswith('/noaa/functions/active_storms/items.json'):
        mock_response = mock.Mock()
        mock_response.json = lambda: [
            {
                '_table_name': 'coneforecastal222020',
                '_timestamp': '2020-11-25T09:26:34.061635Z'
            }
        ]
        return mock_response
    else:
        return original_requests_get(url)


class TestHazardIngestion(TestCase):

    databases = ['default', 'backend']

    def test_hazard_ingestion(self):

        with mock.patch('requests.get', mock_get_geocris_noaa_api):
            call_command('ingest_hazard_data')



