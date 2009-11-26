from django import forms
from django.forms.util import flatatt
from django.utils.html import escape
from django.utils.safestring import mark_safe

class ReadOnlyWidget(forms.Widget):
      
    def __init__(self, display_value=None):
        self.display_value = display_value
        super(ReadOnlyWidget, self).__init__()
  
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        value = self.display_value is not None and self.display_value or value
        return mark_safe("<p %s>%s</p>" % (flatatt(final_attrs), escape(value) or ''))
     
    #def value_from_datadict(self, data, files, name):
    #    return self.original_value

    def _has_changed(self, initial, data):
        return False

class ReadOnlyAdminFields(object):
    def get_form(self, request, obj=None, **kwargs):
        form = super(ReadOnlyAdminFields, self).get_form(request, obj, **kwargs)
 
        if hasattr(self, 'readonly'):
            for field_name in self.readonly:
                if field_name in form.base_fields:
 
                    if hasattr(obj, 'get_%s_display' % field_name):
                        display_value = getattr(obj, 'get_%s_display' % field_name)()
                    else:
                        display_value = None
 
                    form.base_fields[field_name].widget = ReadOnlyWidget(display_value)
                    form.base_fields[field_name].required = False
 
        return form
    