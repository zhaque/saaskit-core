### -*- coding: utf-8 -*- ####################################################

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django_extensions.utils.text import truncate_letters

class SiteAdsense(models.Model):
    
    code = models.TextField(_('adsense code'))
    sites = models.ManyToManyField(Site, related_name="adsenses")
    
    class Meta:
        verbose_name_plural = _('adsenses')
    
    def __unicode__(self):
        return truncate_letters(self.code, 30)
    