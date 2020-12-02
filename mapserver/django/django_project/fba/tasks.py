import logging
from fba.celery import app
from django.core import management

logger = logging.getLogger(__name__)


@app.task(name='fba.process_hazard_event_queue')
def process_hazard_event_queue():
    logger.log(logging.INFO, 'process event queue')
    management.call_command(
        'process_hazard_event_queue'
    )


@app.task
def ingest_boundary_data():
    logger.log(logging.INFO, 'Ingest boundary data')
    management.call_command(
        'ingest_boundary_data'
    )


@app.task
def ingest_building_data():
    logger.log(logging.INFO, 'Ingest boundary data')
    management.call_command(
        'ingest_building_data'
    )


@app.task
def ingest_road_data():
    logger.log(logging.INFO, 'Ingest boundary data')
    management.call_command(
        'ingest_road_data'
    )


@app.task
def ingest_hazard_data():
    logger.log(logging.INFO, 'Ingest boundary data')
    management.call_command(
        'ingest_hazard_data'
    )
