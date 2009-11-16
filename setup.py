### -*- coding: utf-8 -*- ####################################################

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

install_requires = [
        'setuptools',
        'saaskit-muaccounts',
        'Django',
        'python-openid',
        'django-autoslug',
        'django-compress',
        'django-debug-toolbar',
        'django-extensions',
        'django-filter',
        'django-mailer',
        'django-mptt',
        'django-notification',
        'django-oembed',
        'django-perfect404',
        'django-piston',
        'django-rosetta',
        'django-tagging',
        'django-templatesadmin',
        'django-uni-form',
        'django-authopenid',
        'django-notification==0.1.4',
        'app_media',
        'django-ab',
        'django-paypal',
        'django-prepaid',
        'django-quotas',
        'django-pipes',
        'django-sso',
        'django-registration',
        'django-profiles',
        'django-contact-form',
        'django-pagination',
        'django-tinymce',
        'South',
        'html5lib',
        'python-dateutil',
        'sorl-thumbnail',
        'Fabric',
        'PIL',
        'django-friends',
        'gdata',
        'vobject',
        'ybrowserauth',
        'simplejson',
        'django-counter',
        
        'Reportlab',
        'pisa',
        
        'django-frontendadmin==0.3.1',
        'django-email-confirmation',
        
        'saaskit-main-site',
        'saaskit-user-site',
        'saaskit-subscription',
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
        'http://pypi.saaskit.org/Fabric/',
        'http://pypi.saaskit.org/South/',
        'http://pypi.saaskit.org/app-media/',
        'http://pypi.saaskit.org/django-ab/',
        'http://pypi.saaskit.org/django-authopenid/',
        'http://pypi.saaskit.org/django-contact-form/',
        'http://pypi.saaskit.org/django-notification/',
        'http://pypi.saaskit.org/django-paypal/',
        'http://pypi.saaskit.org/django-pipes/',
        'http://pypi.saaskit.org/django-prepaid/',
        'http://pypi.saaskit.org/django-profiles/',
        'http://pypi.saaskit.org/django-quotas/',
        'http://pypi.saaskit.org/django-registration/',
        'http://pypi.saaskit.org/django-sso/',
        'http://pypi.saaskit.org/django-subscription/',
        'http://pypi.saaskit.org/django-frontendadmin/',
        'http://pypi.pinaxproject.com/',
        'http://distfiles.minitage.org/public/externals/minitage/',
]

setup(name="saaskit-core",
            version="0.1",
            description="Core of saaskit",
            author="CrowdSense",
            author_email="admin@crowdsense.com",
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
