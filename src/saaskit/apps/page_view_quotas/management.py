### -*- coding: utf-8 -*- ##

from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_noop as _

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
    
    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("page_view_quotas_almost_ends", 
                _("Page view quota almost ends!"), 
                _("Upgrade your plan to increase quota. You have only %s views." \
                  % settings.GRACE_PAGE_VIEW), default=2)
        notification.create_notice_type("page_view_quotas_ends", 
                _("Page view quota was ended!"), 
                _("Upgrade your plan to increase quota. Every moment your account may be suspended."), default=2)
        notification.create_notice_type("account_suspended_page_view_quotas_ends", 
                _("Site suspended"), 
                _("Your site was suspended."), default=2)
    
    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"
