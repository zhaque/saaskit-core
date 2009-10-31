### -*- coding: utf-8 -*- ####################################################
from django.conf.urls.defaults import *

urlpatterns = patterns('muaccount_content.views',
    (r'^(?P<url>.*)$', 'mu_flatpage'),
)
