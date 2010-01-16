### -*- coding: utf-8 -*- ####################################################

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

install_requires = [
        'setuptools',
        'Django',
        'python-openid',
        'django-autoslug',
        'django-compress',
        'django-debug-toolbar',
        'django-extensions',
        'django-filter',
        'django-mailer',
        'django-mptt',
        'django-oembed',
        'django-piston',
        'django-rosetta',
        'django-tagging',
        'django-templatesadmin',
        'django-authopenid',
        'django-pagination',
        'django-tinymce',
        'South',
        'html5lib',
        'python-dateutil',
        'sorl-thumbnail',
        'PIL==1.1.6',
        'django-friends==0.1.4',
        'gdata',
        'vobject',
        'ybrowserauth',
        'simplejson',
        'django-counter',
        'Reportlab',
        'pisa',
        'django-email-confirmation',
        'PyYAML',

        'Fabric',
        'python-memcached',

        'django-error-capture-middleware',        
        'django-notification',
        'django-paypal',
        'django-frontendadmin',
        'django-profiles',
        'django-registration',
        'django-ab',
        'django-sso',
        'django-uni-form',
        'django-paypal-api',
        'django-pipes',
        'django-contact',
        'django-quotas',
        'app_media',
        'saaskit-main-site',
        'saaskit-user-site',
        'saaskit-muaccounts',
        'saaskit-subscription',
        'saaskit-prepaid',
]

extras_require = dict(
    test = [
        'coverage',
        'windmill',
    ]
)

#AFAIK:
install_requires.extend(extras_require['test'])


dependency_links = [
        'http://pypi.pinaxproject.com/',
        'http://pypi.appspot.com/',
        'http://distfiles.minitage.org/public/externals/minitage/',
]

setup(name="saaskit-core",
            version="1.0",
            description="Software as a Service Core toolkit",
            author="SaaSkit",
            author_email="admin@saaskit.org",
            packages = find_packages('src'),
            package_dir = {'': 'src'},
            include_package_data = True,
            zip_safe = False,
            install_requires = install_requires,
            extras_require = extras_require,
            entry_points="""
              # -*- Entry points: -*-
              """,
            dependency_links = dependency_links,
)
