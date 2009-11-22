from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required

handler404 = 'perfect404.views.page_not_found'

from subscription.models import Transaction

def wrapped_queryset(func, queryset_edit=lambda request, queryset: queryset):
    def wrapped(request, queryset, *args, **kwargs):
        return func(request, queryset=queryset_edit(request, queryset), *args, **kwargs)
    wrapped.__name__ = func.__name__
    return wrapped

urlpatterns = patterns('',
    url(r'^sso/$', 'sso.views.sso', name="sso"),
    (r'^profiles/', include('saaskit_profile.urls')),
    
    (r'^notices/', include('notification.urls')),
    (r'^content/', include('frontendadmin.urls')),
    
)

# serve static files in dev mode
if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
