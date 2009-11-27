### -*- coding: utf-8 -*- ####################################################

from django import template

from django.utils.safestring import mark_safe

from muaccounts.utils import mu_queryset
from muaccount_adsense.models import AdsenseBlock

register = template.Library()  

@register.simple_tag
def adsense(muaccount, name):
    return mark_safe(mu_queryset(muaccount, AdsenseBlock.objects.all(), 'name')\
                     .get(name__exact=name).code)
