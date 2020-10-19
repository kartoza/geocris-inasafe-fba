"""Configuration for production server"""
# noinspection PyUnresolvedReferences
from .prod import *  # noqa
import os

DEBUG = ast.literal_eval(
    os.environ.get('DEBUG', 'False'))

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ABS_PATH('./'), 'db.sqlite3'),
    },
    'backend': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASS'],
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': os.environ['POSTGRES_PORT'],
        'TEST': {
            'NAME': os.environ['POSTGRES_DB'],
        }
    },
}

FIXTURES = '/home/web/fixtures'


if DEBUG:
    LOGGING['handlers']['console']['level'] = 'DEBUG'
    LOGGING['root']['level'] = 'DEBUG'
