from django.conf import settings
from django.conf.urls.defaults import *

def wrapped_queryset(func, queryset_edit=lambda request, queryset: queryset):
    def wrapped(request, queryset, *args, **kwargs):
        return func(request, queryset=queryset_edit(request, queryset), *args, **kwargs)
    wrapped.__name__ = func.__name__
    return wrapped

urlpatterns = patterns('',
    url(r'^sso/$', 'sso.views.sso', name="sso"),
    (r'^content/', include('frontendadmin.urls')),
)

# serve static files in dev mode
if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
