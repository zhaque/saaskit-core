### -*- coding: utf-8 -*- ####################################################

from django.contrib import admin

from muaccount_adsense.models import AdsenseBlock

class AdsenseBlockAdmin(admin.ModelAdmin):
    list_display = ('name', 'muaccount')

admin.site.register(AdsenseBlock, AdsenseBlockAdmin)
