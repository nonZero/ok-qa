from __future__ import absolute_import
import os

from .base import *

ENV = 'LOCAL'
STATIC_S3 = False

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dev.db', # Or path to database file if using sqlite3.
        'USER': '', # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False

LOGGING['handlers']['console']['level'] = 'DEBUG'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if not STATIC_S3:
    STATIC_URL = '/static/'
    STATIC_PATH = '/static/'
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://localhost:9200',
        'INDEX_NAME': 'qa',
    },
}
