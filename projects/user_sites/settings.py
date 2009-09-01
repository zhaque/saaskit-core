from common_settings import *

import os.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

SITE_ID = 2

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+*q3$z(d1@hi^p%645&636$n7r@=w!m)(z9@k9&9s9_7uh%a+s'

MIDDLEWARE_CLASSES += ('muaccounts.middleware.MUAccountsMiddleware',)

TEMPLATE_DIRS = (
    os.path.join(KIT_ROOT, 'templates/user_sites'),
) + TEMPLATE_DIRS
