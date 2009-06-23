# This module is available as common_settings from projects' settings module.
# It contains settings used in all projects.

import os.path
from django.conf import global_settings

KIT_ROOT=os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = os.path.join(KIT_ROOT, 'crowdsense.db')  # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_authopenid.middleware.OpenIDMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'paypal.standard.ipn',
    'registration',
    'django_authopenid',
    'profiles',
    'mptt',
    'pages',
    'notification',
    'mailer',
    'faq',
    'django_pipes',
    'tagging',
    'quotas',
    'muaccounts',
    'subscription',
    'prepaid',
    'crowdsense',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django_authopenid.context_processors.authopenid',
    'pages.context_processors.media',
    )

TEMPLATE_DIRS = ( os.path.join(KIT_ROOT, 'templates'), )

AUTH_PROFILE_MODULE = 'crowdsense.UserProfile'

PAGE_TAGGING = True
PAGE_TINYMCE = False
PAGE_USE_SITE_ID = True
PAGE_LANGUAGES = (                      # need to be filled,
    ('en-us', 'US English'),
    ('en-gb', 'British English'),
)
DEFAULT_PAGE_TEMPLATE = 'page.html'

PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL='example@example.com'
ACCOUNT_ACTIVATION_DAYS=7
LOGIN_REDIRECT_URL = '/'
SUBSCRIPTION_PAYPAL_SETTINGS = {
    'business' : PAYPAL_RECEIVER_EMAIL,
    }

MUACCOUNTS_ROOT_DOMAIN = 'example.com'
# MUACCOUNTS_DEFAULT_DOMAIN = 'www.example.com'
MUACCOUNTS_DEFAULT_URL = 'http://www.example.com:8001/'
MUACCOUNTS_PORT=8000
MUACCOUNTS_IP = '127.0.0.1'
