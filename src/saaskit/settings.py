# This module is available as common_settings from projects' settings module.
# It contains settings used in all projects.

import os.path
from django.conf import global_settings

KIT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = False

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = os.path.join(KIT_ROOT, 'saaskit.db')  # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(KIT_ROOT, 'site_media')
APP_MEDIA_ROOT = MEDIA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

SERVE_MEDIA = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
#   'ab.loaders.load_template_source',
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
   'django.template.loaders.eggs.load_template_source',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'sso.middleware.SingleSignOnMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_authopenid.middleware.OpenIDMiddleware',
    'subscription.middleware.SubscriptionMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'sso.middleware.SingleSignOnMiddleware',
    'muaccount_content.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'saaskit.urls'

INSTALLED_APPS = (
    'saaskit',
                  
    # builtin
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    
    'compress',
    'contact_form',
    'emailconfirmation',
    'registration',
    'django_authopenid',
    'django_extensions',
    'django_pipes',
    'notification',
    'paypal.standard.ipn',
    'perfect404',
    'profiles',
    'sorl.thumbnail',
    'south',
    'sso',
    'tagging',
    'oembed',
    'templatesadmin',
    'uni_form',
    'pagination',
    'app_media',
    'friends',
    'tinymce',
    'frontendadmin',
    'django.contrib.flatpages',
    'django_counter',
    'rosetta',
    
    # own
    'muaccounts',
    'prepaid',
    'quotas',
    'subscription',
    
    # local
    'saaskit_profile',
    'muaccount_content',
    'muaccount_adsense',
    'muaccounts_quotas',
    'page_view_quotas',
    
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django_authopenid.context_processors.authopenid',
    )
TEMPLATE_DIRS = ( os.path.join(KIT_ROOT, 'templates').replace('\\','/'), )

TEST_RUNNER = "saaskit.tests.coverage_runner.run_tests"
COVERAGE_REPORT_PATH = os.path.join(KIT_ROOT, 'coverage_report')

AUTHENTICATION_BACKENDS = ('subscription.backends.UserSubscriptionBackend',)

# Settings for templates editing via django admin

TEMPLATESADMIN_HIDE_READONLY = True
TEMPLATESADMIN_GROUP = 'Editors'
TEMPLATESADMIN_VALID_FILE_EXTENSIONS = (
        'html',
        'css',
        'txt',
        'backup',
   )

TEMPLATESADMIN_EDITHOOKS = (
        'templatesadmin.edithooks.dotbackupfiles.DotBackupFilesHook',
#        'templatesadmin.edithooks.gitcommit.GitCommitHook',
   )

import user_site

TEMPLATESADMIN_TEMPLATE_DIRS = (
      os.path.join(os.path.dirname(user_site.__file__), 'templates').replace('\\','/'),
   ) + TEMPLATE_DIRS

INTERNAL_IPS = ( '127.0.0.1', )

AUTH_PROFILE_MODULE = 'saaskit_profile.UserProfile'

SSO_SECRET = "6O4nVw|~w't2mxV%oeSUDew{9zhN.\"lY1T.xi9nmZL+lNxGlr@K5+~>NnLMHNAN]57s"

COMPRESS = False
COMPRESS_VERSION = False

_default_css_files = ('saaskit/yui-app-theme/yuiapp.css',
                      'saaskit/auth/css/openid.css',
                      'uni_form/uni_form/uni-form-generic.css',
                      'uni_form/uni_form/uni-form.css',
                      'saaskit/css/friends.css',
                      'saaskit/css/subscription.css',
                      'saaskit/css/forms.css',
                      )

COMPRESS_CSS = {                        # different themes for MUAs
    'all' : {
        'name' : 'Default theme',
        'source_filenames' : _default_css_files,
        'output_filename' : 'style.css'},
    }
COMPRESS_JS = {
    'all' : {
        'source_filenames' : (# 'authopenid/js/jquery-1.3.2.min.js',
                              'uni_form/uni_form/uni-form.jquery.js',
                              ),
        'output_filename' : 'scripts.js'},
    }

ACCOUNT_ACTIVATION_DAYS=7
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/signin/'

SSO_URL = '/sso/'
LOGOUT_URL = '/accounts/signout/'


QUOTAS = {
    'muaccount_members' : (3, 10, 50),
    'muaccounts': (1, 5),
    'page_views': (10000, 10000000),
    }

GRACE_PAGE_VIEW = 1000

MUACCOUNTS_ROOT_DOMAIN = 'example.com'
MUACCOUNTS_DEFAULT_URL = 'http://www.example.com:8001/'
MAIN_SITE_PORT = 8001
MUACCOUNTS_PORT = 8000

MUACCOUNTS_IP = '127.0.0.1'
MUACCOUNTS_MAIN_URLCONF = 'main_site.urls'
MUACCOUNTS_USERSITE_URLCONF = 'user_site.urls'
MUACCOUNTS_SUBDOMAIN_STOPWORDS = (r"^www$", r"^support$", r"^lab$", r"^labs$", r"^dev$", r"^development$", r"^ops$", r"^operations$", r"^corp$", r"^media$", r"^assets$", r"^mail$", r"^docs$", r"^calendar$", r"^contacts$", r"^feedback$", r"^chat$")
MUACCOUNTS_THEMES = (
    # color css
    ('color_scheme', 'Color scheme', (
        ('aqua', 'Aqua', 'saaskit/yui-app-theme/aqua.css'),
        ('green', 'Green', 'saaskit/yui-app-theme/green.css'),
        ('purple', 'Purple', 'saaskit/yui-app-theme/purple.css'),
        ('red', 'Red', 'saaskit/yui-app-theme/red.css'),
        ('tan-blue', 'Tan Blue', 'saaskit/yui-app-theme/tan_blue.css'),
        ('default', 'CrowdSense', 'saaskit/css/default.css'),
        ('fireflynight', 'Firefly Night', 'saaskit/css/fireflynight.css'),
        ('grayscale', 'Grayscale', 'saaskit/css/grayscale.css'),
        ('graygreen', 'Grayscale Green', 'saaskit/css/gray-green.css'),
        ('overcast', 'Overcast', 'saaskit/css/overcast.css'),
        ('sunshine', 'Sunshine', 'saaskit/css/sunshine.css'),
        )),
    # <body> id
    ('page_width', 'Page widgh', (
        ('doc3', '100% fluid'),
        ('doc', '750px centered'),
        ('doc2', '950px centered'),
        ('doc4', '974px fluid'),
        )),
    # Outermost <div> class
    ('layout', 'Layout', (
        ('yui-t6', 'Right sidebar, 300px'),
        ('yui-t1', 'Left sidebar, 160px'),
        ('yui-t2', 'Left sidebar, 180px'),
        ('yui-t3', 'Left sidebar, 300px'),
        ('yui-t4', 'Right sidebar, 180px'),
        ('yui-t5', 'Right sidebar, 240px'),
        ('yui-t0', 'Single Column'),
        )),
    # <body> class
    ('rounded_corners', 'Rounded corners', (
        ('on', 'On', 'rounded'),
        ('off', 'Off', ''),
        )),
    )

ugettext = lambda s: s

LANGUAGES = (
    ('en', ugettext('English')),
    ('de', ugettext('German')),
    ('fr', ugettext('French')),
    ('ru', ugettext('Russian')),
)

# Prepare CSS files for configured color schemes
for codename, _, css_file in MUACCOUNTS_THEMES[0][2]:
     COMPRESS_CSS[codename] = {
         'source_filenames' : ( (_default_css_files[0], css_file,)
                                + _default_css_files[1:] ),
         'output_filename' : 'style.%s.css' % codename,
         }

SITE_NAME = 'Saaskit'
DEFAULT_FROM_EMAIL = 'support@example.com'
CONTACT_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_SUBJECT_PREFIX = "[SaaSKit] "
EMAIL_CONFIRMATION_DAYS = 2

TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced", 'relative_urls': True, 
    'height': '700px', 'width': '79%', 
    'theme_advanced_toolbar_location' : "top",
}
TINYMCE_JS_ROOT = os.path.join(MEDIA_ROOT, 'saaskit/js/tiny_mce')

PAYPAL_PRO = False

#Dummy paypal settings
PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL='example@example.com'
SUBSCRIPTION_PAYPAL_SETTINGS = {
    'business' : PAYPAL_RECEIVER_EMAIL,
    }

# Website payments Pro settings
PAYPAL_WPP_USER = ""
PAYPAL_WPP_PASSWORD = ""
PAYPAL_WPP_SIGNATURE = ""


# Local settings for development / production
try:
     from local_settings import *
except ImportError:
     pass

if PAYPAL_PRO:
    INSTALLED_APPS += ('paypal.standard', 'paypal.pro')

TINYMCE_JS_URL = '%s/saaskit/js/tiny_mce/tiny_mce.js' % MEDIA_URL
