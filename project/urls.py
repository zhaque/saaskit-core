from django.conf import settings
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

import signal_handlers
signal_handlers.install()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', dict(template='index.html')),
    (r'^accounts/', include('django_authopenid.urls')),
    (r'^accounts/mua/', include('muaccounts.urls')),
    (r'^profiles/', include('profiles.urls')),
    (r'^sub/', include('subscription.urls')),
    (r'^pages/', include('pages.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)

# serve static files in debug mode
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
