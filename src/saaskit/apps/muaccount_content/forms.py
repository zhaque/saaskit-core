### -*- coding: utf-8 -*- ####################################################

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

from tinymce import widgets as tinymce_widgets
from uni_form.helpers import FormHelper, Submit

import muaccounts.forms
from muaccount_content.models import MUFlatPage
from saaskit.widgets.readonlyhidden import ReadOnlyWidgetWithHidden

class MuFlatpageAddForm(muaccounts.forms.AddFormMixin, forms.ModelForm):
    
    # this displays how to attach a formHelper to your forms class.
    helper = FormHelper()
    helper.add_input(Submit('submit',_('Create')))
    helper.add_input(Submit('_cancel',_('Cancel')))
    is_multipart = True
    
    class Meta:
        model = MUFlatPage
    
    def __init__(self, *args, **kwargs):
        super(MuFlatpageAddForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = tinymce_widgets.TinyMCE()
        self.fields['sites'].widget = forms.MultipleHiddenInput()
    

class MuFlatpageChangeForm(muaccounts.forms.ChangeFormMixin, MuFlatpageAddForm):
    
    def __init__(self, *args, **kwargs):
        super(MuFlatpageChangeForm, self).__init__(*args, **kwargs)
        if self.instance.has_default():
            self.fields['title'].widget = ReadOnlyWidgetWithHidden()
            self.fields['url'].widget = ReadOnlyWidgetWithHidden()
