### -*- coding: utf-8 -*- ##

DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = '{{ POSTGRES_USER }}'
DATABASE_USER = '{{ POSTGRES_USER }}'
DATABASE_PASSWORD = '{{ POSTGRES_PASSWORD }}'
DATABASE_HOST = ''
DATABASE_PORT = '5432'

PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL='{{ PAYPAL_EMAIL }}'
SUBSCRIPTION_PAYPAL_SETTINGS = {
    'business' : PAYPAL_RECEIVER_EMAIL,
    }

MUACCOUNTS_ROOT_DOMAIN = '{{ host_string }}'
MUACCOUNTS_DEFAULT_URL = 'http://{{host_string }}/'
MUACCOUNTS_PORT=80

BUY_SITE_URL = 'http://{{ host_string }}/subscription/'

MEDIA_URL = 'http://assets.{{ host_string }}/'
ADMIN_MEDIA_PREFIX = 'http://assets.{{ host_string }}/admin/'

DEFAULT_FROM_EMAIL = 'support@{{ host_string }}'
CONTACT_EMAIL = DEFAULT_FROM_EMAIL

#SESSION_COOKIE_DOMAIN = '.{{ host_string }}'
