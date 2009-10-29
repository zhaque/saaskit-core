from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_noop as _

from saaskit_profile import models

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
    
    def create_member_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("welcome", _("Welcome to CrowdSense Starter Kit!"), _("you have successfully registered"), default=2)
        notification.create_notice_type("member_add", _("Added to site"), _("you were added as a member to a site"), default=2)
        notification.create_notice_type("member_remove", _("Removed from site"), _("you were removed from membership in a site"), default=2)
    
    signals.post_syncdb.connect(create_member_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"
