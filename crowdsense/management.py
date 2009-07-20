from django.conf import settings
from django.utils.translation import ugettext_noop as _
from django.db.models import signals
 
from notification import models as notification
 
def create_notice_types(app, created_models, verbosity, **kwargs):
    for type, display, description in settings.NOTICE_TYPES:
        notification.create_notice_type(type, display, description)

signals.post_syncdb.connect(create_notice_types, sender=notification)
