from celery.schedules import crontab
import os
import ast

SCHEDULE_HAZARD_EVENT_QUEUE = ast.literal_eval(os.environ.get(
    'SCHEDULE_HAZARD_EVENT_QUEUE', '{}'))
# Default to minutely
SCHEDULE_HAZARD_EVENT_QUEUE = SCHEDULE_HAZARD_EVENT_QUEUE or {
    'minute': '*'
}

SCHEDULE_INGEST_BOUNDARY_DATA = ast.literal_eval(os.environ.get(
    'SCHEDULE_INGEST_BOUNDARY_DATA', '{}'
))
SCHEDULE_INGEST_BOUNDARY_DATA = SCHEDULE_INGEST_BOUNDARY_DATA or {
    'day_of_week': '*'
}

SCHEDULE_INGEST_BUILDING_DATA = ast.literal_eval(os.environ.get(
    'SCHEDULE_INGEST_BUILDING_DATA', '{}'
))
SCHEDULE_INGEST_BUILDING_DATA = SCHEDULE_INGEST_BUILDING_DATA or {
    'day_of_week': '*'
}

SCHEDULE_INGEST_ROAD_DATA = ast.literal_eval(os.environ.get(
    'SCHEDULE_INGEST_ROAD_DATA', '{}'
))
SCHEDULE_INGEST_ROAD_DATA = SCHEDULE_INGEST_ROAD_DATA or {
    'day_of_week': '*'
}

SCHEDULE_INGEST_HAZARD_DATA = ast.literal_eval(os.environ.get(
    'SCHEDULE_INGEST_HAZARD_DATA', '{}'
))
SCHEDULE_INGEST_HAZARD_DATA = SCHEDULE_INGEST_HAZARD_DATA or {
    'day_of_week': '*'
}

CELERYBEAT_SCHEDULE = {
    'hazard_event_queue': {
        'task': 'fba.process_hazard_event_queue',
        'schedule': crontab(**SCHEDULE_HAZARD_EVENT_QUEUE),
    },
    'ingest_boundary_data': {
        'task': 'fba.tasks.ingest_boundary_data',
        'schedule': crontab(**SCHEDULE_INGEST_BOUNDARY_DATA)
    },
    'ingest_building_data': {
        'task': 'fba.tasks.ingest_building_data',
        'schedule': crontab(**SCHEDULE_INGEST_BUILDING_DATA)
    },
    'ingest_road_data': {
        'task': 'fba.tasks.ingest_road_data',
        'schedule': crontab(**SCHEDULE_INGEST_ROAD_DATA)
    },
    'ingest_hazard_data': {
        'task': 'fba.tasks.ingest_hazard_data',
        'schedule': crontab(**SCHEDULE_INGEST_HAZARD_DATA)
    }
}

CELERY_TIMEZONE = 'UTC'

#BROKER_URL = 'memory://localhost'
BROKER_URL = 'amqp://guest:guest@rabbitmq'
CELERY_RESULT_BACKEND = 'rpc://'

