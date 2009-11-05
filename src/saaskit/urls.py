from django.conf import settings
from django.conf.urls.defaults import *

handler404 = 'perfect404.views.page_not_found'

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^sso/$', 'sso.views.sso', name="sso"),
    (r'^accounts/', include('django_authopenid.urls')),
    (r'^profiles/', include('saaskit_profile.urls')),
    url(r'^subscription/(?P<object_id>\d+)/$', 'subscription.views.subscription_detail', 
     {'payment_method':'pro' if settings.PAYPAL_PRO else 'standard'}, name='subscription_detail'),
    (r'^subscription/', include('subscription.urls')),
    (r'^notices/', include('notification.urls')),
    (r'^content/', include('frontendadmin.urls')),
)

# serve static files in dev mode
if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
