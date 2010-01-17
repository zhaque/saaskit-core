### -*- coding: utf-8 -*- ####################################################

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

install_requires = [
        'setuptools',
        'Django==1.1.1',
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
        'django-pagination',
        'django-tinymce',
        'django-email-confirmation',
        'django-friends==0.1.4',
        'django-counter',
        'South',
        'html5lib',
        'python-dateutil',
        'sorl-thumbnail',
        'PIL==1.1.6',
        'gdata',
        'vobject',
        'ybrowserauth',
        'simplejson',
        'Reportlab',
        'pisa',
        'PyYAML',
        'python-memcached',

        'Fabric',

        'app-media',
        'django-ab',
        'django-authopenid',
        'django-contact',
        'django-error-capture-middleware',
        'django-frontendadmin',
        'django-notification', 
        'django-paypal',
        'django-paypal-api',
        'django-pipes',
        'django-profiles',
        'django-quotas',
        'django-registration',
        'django-sso',
        'django-uni-form',

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
