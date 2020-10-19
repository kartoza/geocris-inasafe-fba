import logging

from django import test

from fba.models.views import CensusPopulationSummaryDistrictStats

logger = logging.getLogger(__name__)


class TestSummaryStats(test.LiveServerTestCase):

    databases = ['default', 'backend']

    def test_population_stats(self):
        objects = CensusPopulationSummaryDistrictStats.objects.filter(flood_event__id=69)
        logger.debug(objects)
        logger.debug(objects[0])
