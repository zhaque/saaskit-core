### -*- coding: utf-8 -*- ####################################################

from django import forms
from django.utils.translation import ugettext_lazy as _

from uni_form.helpers import FormHelper, Submit

import muaccounts.forms
from saaskit.widgets.readonlyhidden import ReadOnlyWidgetWithHidden

from muaccount_adsense.models import AdsenseBlock

class AdsenseBlockChangeForm(muaccounts.forms.AddFormMixin, muaccounts.forms.ChangeFormMixin, forms.ModelForm):
    
    # this displays how to attach a formHelper to your forms class.
    helper = FormHelper()
    helper.add_input(Submit('submit',_('Submit')))
    helper.add_input(Submit('_cancel',_('Cancel')))
    is_multipart = True
    
    class Meta:
        model = AdsenseBlock
    
    def __init__(self, *args, **kwargs):
        super(AdsenseBlockChangeForm, self).__init__(*args, **kwargs)
        if self.instance.has_default():
            self.fields['name'].widget = ReadOnlyWidgetWithHidden()
