### -*- coding: utf-8 -*- ####################################################

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

install_requires = [
        'Django==1.1.1',
        'PIL==1.1.6',
        'PyYAML==3.09',
        'South==0.6.2',
        'django-autoslug==1.3.8',
        'django-compress==1.0.1',
        'django-counter==0.1.5',
        'django-debug-toolbar==0.8.1',
        'django-email-confirmation==0.2.dev1',
        'django-extensions==0.4.1',
        'django-filter==0.5.2',
        'django-friends==0.1.4',
        'django-mailer==0.2.0dev1',
        'django-mptt==0.3-pre',
        'django-oembed==0.1.1',
        'django-pagination==1.0.5.1',
        'django-piston==0.2.2',
        'django-rosetta==0.5.1',
        'django-tagging==0.3',
        'django-templatesadmin==0.6',
        'django-tinymce==1.5',
        'gdata==2.0.6',
        'html5lib==0.11.1',
        'pisa==3.0.32',
        'python-dateutil==1.4.1',
        'python-memcached==1.45',
        'python-openid==2.2.4',
        'Reportlab==2.3',
        'setuptools==0.6c11',
        'simplejson==2.0.9',
        'sorl-thumbnail==3.2.5',
        'vobject==0.8.1c',
        'ybrowserauth==1.2',

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
        'coverage==3.2',
        'windmill==1.3',
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
