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


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
#   'ab.loaders.load_template_source',
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#   'django.template.loaders.eggs.load_template_source',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_authopenid.middleware.OpenIDMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'sso.middleware.SingleSignOnMiddleware',
#   'debug_toolbar.middleware.DebugToolbarMiddleware',
#   'ab.middleware.ABMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    # builtin
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    # third-party
    'compress',
    'contact_form',
    'django_authopenid',
    'django_extensions',
    'django_pipes',
    'notification',
    'paypal.standard.ipn',
    'perfect404',
    'profiles',
    'registration',
    'sorl.thumbnail',
    'south',
    'sso',
    'tagging',
    'oembed',
    'templatesadmin', 
    'uni_form', 
    # 3rd party apps currently not used
    # 'ab',
    # 'filter',
    # 'rosetta',
    # 'autoslug',
    # 'mailer',
    # 'mptt',
    # 'piston',
    # 'pages', 
    # own
    'muaccounts',
    'prepaid',
    'quotas',
    'subscription',
    # local
    'saaskit',
    # only in development 
    #'debug_toolbar',

)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django_authopenid.context_processors.authopenid',
#   'pages.context_processors.media',
    )

TEMPLATE_DIRS = ( os.path.join(KIT_ROOT, 'templates'), )

# Settings for templates editing via django admin
 
TEMPLATESADMIN_HIDE_READONLY = True 
TEMPLATESADMIN_GROUP = 'Editors'
TEMPLATESADMIN_VALID_FILE_EXTENSIONS = (
        'html', 
        'css', 
        'txt',
        'backup'
   )

TEMPLATESADMIN_EDITHOOKS = (    
        'templatesadmin.edithooks.dotbackupfiles.DotBackupFilesHook',
#        'templatesadmin.edithooks.gitcommit.GitCommitHook',
   )

TEMPLATESADMIN_TEMPLATE_DIRS = (
      ( os.path.join(KIT_ROOT, 'templates'), ) 
   )

INTERNAL_IPS = ( '127.0.0.1', )

AUTH_PROFILE_MODULE = 'saaskit.UserProfile'

SSO_SECRET = "6O4nVw|~w't2mxV%oeSUDew{9zhN.\"lY1T.xi9nmZL+lNxGlr@K5+~>NnLMHNAN]57s"

COMPRESS = False 
COMPRESS_VERSION = False 

NOTICE_TYPES = (
     ("welcome", "Welcome to CrowdSense Starter Kit!", "you have successfully registered"),
     ("member_add", "Added to site", "you were added as a member to a site"),
     ("member_remove", "Removed from site", "you were removed from membership in a site"),
     )

_default_css_files = ('yui-app-theme/yuiapp.css',
                      'authopenid/css/openid.css',
                      'uni_form/uni-form-generic.css',
                      'uni_form/uni-form.css',
                      )

COMPRESS_CSS = {                        # different themes for MUAs
    'all' : {
        'name' : 'Default theme',
        'source_filenames' : _default_css_files,
        'output_filename' : 'style.css'},
    }
COMPRESS_JS = {
    'all' : {
        'source_filenames' : ('authopenid/js/jquery-1.3.2.min.js',
                              'uni_form/uni-form.jquery.js',
                              ),
        'output_filename' : 'scripts.js'},
    }

PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL='example@example.com'
ACCOUNT_ACTIVATION_DAYS=7
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/signin/'
SUBSCRIPTION_PAYPAL_SETTINGS = {
    'business' : PAYPAL_RECEIVER_EMAIL,
    }

QUOTAS = {
    'muaccount_members' : (3, 10, 50),
    }

MUACCOUNTS_ROOT_DOMAIN = 'example.com'
MUACCOUNTS_DEFAULT_URL = 'http://www.example.com:8001/'
MUACCOUNTS_PORT=8000
MUACCOUNTS_IP = '127.0.0.1'
MUACCOUNTS_USERSITE_URLCONF = 'main.urls_usersite'
MUACCOUNTS_SUBDOMAIN_STOPWORDS = '(r"^www$", r"^support$", r"^lab$", r"^labs$", r"^dev$", r"^development$", r"^ops$", r"^operations$", r"^corp$", r"^media$", r"^assets$", r"^mail$", r"^docs$", r"^calendar$", r"^contacts$", r"^feedback$", r"^chat$")'
MUACCOUNTS_THEMES = (
    # color css
    ('color_scheme', 'Color scheme', (
        ('aqua', 'Aqua', 'yui-app-theme/aqua.css'),
        ('green', 'Green', 'yui-app-theme/green.css'),
        ('purple', 'Purple', 'yui-app-theme/purple.css'),
        ('red', 'Red', 'yui-app-theme/red.css'),
        ('tan-blue', 'Tan Blue', 'yui-app-theme/tan_blue.css'),
	('default', 'CrowdSense', 'saaskit/css/default.css'),
	('fireflynight', 'Firefly Night', 'saaskit/css/fireflynight.css'),
        ('freshair', 'Fresh Air', 'saaskit/css/freshair.css'),
	('girly', 'Girly', 'saaskit/css/girly.css'),
	('grayscale', 'Grayscale', 'saaskit/css/grayscale.css'),
	('grayscalem', 'Grayscale Modified', 'saaskit/css/grayscalemodified.css'),
	('overcast', 'Overcast', 'saaskit/css/overcast.css'),
	('pepper', 'Pepper', 'saaskit/css/pepper.css'),
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

# Prepare CSS files for configured color schemes
for codename, _, css_file in MUACCOUNTS_THEMES[0][2]:
     COMPRESS_CSS[codename] = {
         'source_filenames' : ( (_default_css_files[0], css_file,)
                                + _default_css_files[1:] ),
         'output_filename' : 'style.%s.css' % codename,
         }

# django-page-cms settings currently disabled, to enable un-comment middleware as well as installed apps and settings below
 
# PAGE_TAGGING = True
# PAGE_TINYMCE = False
# PAGE_USE_SITE_ID = True
# PAGE_LANGUAGES = (
#    ('en-gb', 'English'),
# )
# PAGE_UNIQUE_SLUG_REQUIRED = True
# DEFAULT_PAGE_TEMPLATE = 'page.html'
# PAGE_TEMPLATES = (
#    ('page-templates/single-body.html', 'Single body'),
#    ('page-templates/before-and-after.html', 'Content before and after dynamic content'),
# )

# Local settings for development / production
try:
     from local_settings import *
except ImportError:
     pass
