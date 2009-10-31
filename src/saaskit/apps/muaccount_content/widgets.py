from django import forms
from django.forms.util import flatatt
from django.utils.html import escape
from django.utils.safestring import mark_safe

from answers.external.readonly import ReadOnlyWidget

class ReadOnlyWidgetWithHidden(ReadOnlyWidget):
    
    def render(self, name, value, attrs=None):
        return super(ReadOnlyWidgetWithHidden, self).render(name, value, attrs) + forms.HiddenInput().render(name, value, attrs)
    