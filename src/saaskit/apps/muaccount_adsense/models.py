### -*- coding: utf-8 -*- ####################################################

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from muaccounts.models import MUAccount

class AdsenseBlock(models.Model):
    muaccount = models.ForeignKey(MUAccount, related_name="adsenses", blank=True, null=True)
    name = models.CharField(max_length=100)
    code = models.TextField(blank=True)
    
    class Meta:
        verbose_name = _('Adsense block')
        verbose_name_plural = _('Adsense blocks')
        ordering = ('muaccount', 'name')
    
    def has_default(self):
        return self.__class__.objects.filter(muaccount__exact=None, 
                                             name__exact=self.name, 
                                             ).count()
