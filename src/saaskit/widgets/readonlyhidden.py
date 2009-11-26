from django import forms

from readonly import ReadOnlyWidget

class ReadOnlyWidgetWithHidden(ReadOnlyWidget):
    
    def render(self, name, value, attrs=None):
        return super(ReadOnlyWidgetWithHidden, self).render(name, value, attrs) + forms.HiddenInput().render(name, value, attrs)
    