# Django settings for okqa project.
import os
from unipath import FSPath as Path
import dj_database_url

PROJECT_DIR = Path(__file__).absolute().ancestor(2)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS
INTERNAL_IPS = ('127.0.0.1',)

# TODO: test if the next line is good for us
# SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
TIME_ZONE = 'Asia/Jerusalem'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'he'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = PROJECT_DIR.child('media')
STATIC_ROOT = PROJECT_DIR.child('static_root')
STATICFILES_ROOT = PROJECT_DIR.child('static')

STATICFILES_DIRS = [
    (subdir, str(STATICFILES_ROOT.child(subdir))) for subdir in
    ['css', 'img', 'js']]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
SECRET_KEY = "'piotu34fh89v67b4c2y0[R89N21CB[YUIP'NXREQL;BYCW9"

FIXTURE_DIRS = ("fixtures", )
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'bootstrap_pagination.middleware.PaginationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'okqa.urls'

TEMPLATE_DIRS = (
    PROJECT_DIR.child('templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    'okqa.party.context_processors.forms',
    'social_auth.context_processors.social_auth_by_name_backends',
    )
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'django_extensions',
    'django_nose',
    'taggit',
    'registration',
    'social_auth',
    'haystack',
    'south',
    'debug_toolbar',
    'crispy_forms',
    'storages',
    'gunicorn',
    'bootstrap_pagination',
    'okqa.qa',
    'okqa.user',
    'okqa.party',
    'okqa.taggit_autosuggest',
    'okqa.emails',
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.
LOGIN_REDIRECT_URL = '/'

CANDIDATES_GROUP_NAME = "candidates"


DEFAULT_FROM_EMAIL = 'okqa@hasadna.org.il'

AUTH_PROFILE_MODULE = 'user.UserProfile'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

SITE_ID = os.environ.get('SITE_ID', 1)

TWITTER_CONSUMER_KEY         = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET      = os.environ.get('TWITTER_CONSUMER_SECRET')
FACEBOOK_APP_ID              = os.environ.get('FACEBOOK_APP_ID')
FACEBOOK_API_SECRET          = os.environ.get('FACEBOOK_API_SECRET')
GOOGLE_OAUTH2_CLIENT_ID      = os.environ.get('GOOGLE_OAUTH2_CLIENT_ID')
GOOGLE_OAUTH2_CLIENT_SECRET  = os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET')

