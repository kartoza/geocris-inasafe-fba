# coding=utf-8

"""Project level settings.

Adjust these values as needed but don't commit passwords etc. to any public
repository!
"""

import os  # noqa
from django.utils.translation import ugettext_lazy as _
from .contrib import *  # noqa

# Due to profile page does not available,
# this will redirect to home page after login
from .utils import ABS_PATH
import ast

LOGIN_REDIRECT_URL = '/'

# How many versions to list in each project box
PROJECT_VERSION_LIST_SIZE = 10

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

SOUTH_TESTS_MIGRATE = False

# Set languages which want to be translated
LANGUAGES = (
    ('en', _('English')),
)

# Set storage path for the translation files
LOCALE_PATHS = (ABS_PATH('locale'),)

INSTALLED_APPS += (
    'mapserver',
)

MAPSERVER_PUBLIC_WMS_URL = os.environ.get('MAPSERVER_PUBLIC_WMS_URL', None)
MAPSERVER_PUBLIC_OWS_URL = os.environ.get('MAPSERVER_PUBLIC_OWS_URL', None)
MAPSERVER_PUBLIC_SLD_URL = os.environ.get('MAPSERVER_PUBLIC_SLD_URL', None)
FIXTURES = ABS_PATH('../../fixtures')
# Specify settings to ignore Python Requests SSL verification
REQUESTS_SSL_VERIFY = ast.literal_eval(os.environ.get('REQUESTS_SSL_VERIFY', 'False'))
