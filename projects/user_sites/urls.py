from django.conf import settings
from django.conf.urls.defaults import *

handler404 = 'perfect404.views.page_not_found'

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.direct_to_template', dict(template='index.html'), name='notification_notices'),
    url(r'^sso/$', 'sso.views.sso', name="sso"),
    (r'^sorry/$', 'django.views.generic.simple.direct_to_template', dict(template='account_nam.html'), 'muaccounts_not_a_member'),
    (r'^accounts/', include('django_authopenid.urls')),
    (r'^admin/', include('muaccounts.urls')),
    url(r'^extend/general/$', 'django.views.generic.simple.direct_to_template', dict(template='manage_general.html')),
    url(r'^extend/themes/$', 'django.views.generic.simple.direct_to_template', dict(template='manage_themes.html')),
    url(r'^extend/users/$', 'django.views.generic.simple.direct_to_template', dict(template='manage_users.html')),
    url(r'^extend/advanced/$', 'django.views.generic.simple.direct_to_template', dict(template='manage_advanced.html')),
    url(r'^extend/apps/$', 'django.views.generic.simple.direct_to_template', dict(template='manage_apps.html')),
)

# serve static files in debug mode
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
