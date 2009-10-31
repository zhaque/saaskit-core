### -*- coding: utf-8 -*- ####################################################

from django.contrib import admin
from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _

from tinymce import widgets as tinymce_widgets

from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin

from muaccount_content.models import MUFlatPage

class MuFlatpageForm(FlatpageForm):
    class Meta:
        model = MUFlatPage

class MuFlatPageAdmin(FlatPageAdmin):
    form = MuFlatpageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites', 'muaccount')}),
        (_('Advanced options'), {'classes': ('collapse',), 'fields': ('enable_comments', 'registration_required', 'template_name', 'show_link')}),
    )
    
    formfield_overrides = {
        models.TextField: {'widget': tinymce_widgets.AdminTinyMCE},
    }

admin.site.unregister(FlatPage)
admin.site.register(MUFlatPage, MuFlatPageAdmin)
