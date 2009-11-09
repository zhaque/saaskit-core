from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required

handler404 = 'perfect404.views.page_not_found'

from django.contrib import admin
admin.autodiscover()

from subscription.models import Transaction

from pdf_app.decorators import pdf_response

def wrapped_queryset(func, queryset_edit=lambda request, queryset: queryset):
    def wrapped(request, queryset, *args, **kwargs):
        return func(request, queryset=queryset_edit(request, queryset), *args, **kwargs)
    
    return wrapped

invoice_info = {
    'template_object_name': 'transaction', 
    'queryset': Transaction.objects.filter(event__exact='subscription payment').select_related()
}

invoice_listing_info = {'template_name': 'subscription/invoice_history.html'}
invoice_listing_info.update(invoice_info)

invoice_detail_info = {'template_name': 'subscription/invoice.html'}
invoice_listing_info.update(invoice_info)

invoice_queryset_wrapper = lambda request, queryset: queryset.filter(user=request.user)

urlpatterns = patterns('',
    url(r'^sso/$', 'sso.views.sso', name="sso"),
    (r'^accounts/', include('django_authopenid.urls')),
    (r'^profiles/', include('saaskit_profile.urls')),
    
    url(r'^subscription/(?P<object_id>\d+)/$', 'subscription.views.subscription_detail', 
        {'payment_method':'pro' if settings.PAYPAL_PRO else 'standard'}, 
        name='subscription_detail'),
     
    url(r'^subscription/invoice/$', 
        login_required(wrapped_queryset(object_list, invoice_queryset_wrapper)),
        invoice_listing_info, name='invoice_listing'),
    
    url(r'^subscription/invoice/(?P<object_id>[\d]+)/$', 
        pdf_response(login_required(wrapped_queryset(object_detail, invoice_queryset_wrapper))),
        invoice_detail_info, name='invoice_detail'),
    
    (r'^subscription/', include('subscription.urls')),
    (r'^notices/', include('notification.urls')),
    (r'^content/', include('frontendadmin.urls')),
)

# serve static files in dev mode
if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
