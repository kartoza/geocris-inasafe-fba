import logging
from datetime import timedelta

from django import test

from fba.models.all import HazardMap, HazardArea, HazardAreas
from fba.models.hazard_event import HazardEvent

logger = logging.getLogger(__name__)


class TestGenerateMultipleHazard(test.LiveServerTestCase):
    databases = ['default', 'backend']

    def test_delete_test_hazard(self):
        events: [HazardEvent] = HazardEvent.objects.filter(notes='[test]')
        event: HazardEvent
        area: HazardArea
        areas: HazardAreas
        for event in events:
            for areas in event.hazard_map.hazardareas_set.all():
                area = areas.flooded_area
                areas.delete()
                area.delete()

            hazard_map: HazardMap = event.hazard_map
            spreadsheet = event.spreadsheetreports_set.first()
            spreadsheet.delete()
            event.delete()
            hazard_map.delete()

    def test_generate_hazard(self):
        event: HazardEvent = HazardEvent.objects.order_by(
            '-forecast_date').first()
        hazard_map = event.hazard_map
        hazard_areas = hazard_map.hazardareas_set

        # Create a new hazard map
        new_map = HazardMap.objects.create(
            notes=hazard_map.notes,
            measuring_station=hazard_map.measuring_station,
            place_name=hazard_map.place_name,
            return_period=hazard_map.return_period
        )

        # Create new hazard area
        area: HazardArea
        for area in [a.flooded_area for a in hazard_areas.all()]:
            area = HazardArea.objects.create(
                depth_class=area.depth_class,
                geometry=area.geometry
            )
            HazardAreas.objects.create(
                flood_map=new_map,
                flooded_area=area
            )
        # Create new hazard event
        new_event = HazardEvent.objects.create(
            hazard_map=new_map,
            acquisition_date=event.acquisition_date + timedelta(days=1),
            forecast_date=event.forecast_date + timedelta(days=1),
            source=event.source,
            notes='[test]',
            link=event.link,
            trigger_status=event.trigger_status,
            progress=event.progress,
            hazard_type=event.hazard_type
        )
