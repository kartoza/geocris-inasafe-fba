# coding=utf-8

"""Project level settings."""
from .project import *  # noqa

ALLOWED_HOSTS = ['*']

# Comment if you are not running behind proxy
USE_X_FORWARDED_HOST = True

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

SERVER_EMAIL = 'meomancer@gmail.com'

# Setup email
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_FROM', 'meomancer@gmail.com')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.csir.co.za')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 25))
EMAIL_HOST_USER = 'user@do.ma.in'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_TLS = False
EMAIL_SUBJECT_PREFIX = ''
