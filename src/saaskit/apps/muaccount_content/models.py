### -*- coding: utf-8 -*- ####################################################

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.query import Q
from django.contrib.flatpages.models import FlatPage

from muaccounts.models import MUAccount

class MUFlatPage(FlatPage):
    muaccount = models.ForeignKey(MUAccount, related_name="muflatpages", blank=True, null=True)
    show_link = models.BooleanField(_("show link"), default=True)
    order = models.IntegerField(_('order'), default=1)
    active = models.BooleanField(_("active"), default=True)
    use_default = models.BooleanField(_("use default"), default=False)
    
    class Meta:
        verbose_name_plural = _('flat pages')
        #unique_together = ('url', 'muaccount')
        ordering = ('muaccount', 'url')
    
    def has_default(self):
        return self.__class__.objects.filter(muaccount__exact=None, 
                                             url__exact=self.url, 
                                             sites__id__exact=settings.SITE_ID
                                             ).count()


def mu_queryset(muaccount, queryset, field):
    customized = queryset.filter(muaccount=muaccount)
    return queryset.filter(Q(muaccount__exact=None) | Q(muaccount=muaccount))\
                        .exclude(muaccount__exact=None, 
                 **{'%s__in' % field: customized.values_list(field, flat=True),})
    