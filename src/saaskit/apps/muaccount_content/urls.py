### -*- coding: utf-8 -*- ####################################################
from django.conf.urls.defaults import *

urlpatterns = patterns('muaccount_flatpages.views',
    (r'^(?P<url>.*)$', 'mu_flatpage'),
)
