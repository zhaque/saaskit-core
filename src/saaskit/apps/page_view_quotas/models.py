### -*- coding: utf-8 -*- ####################################################

from django.db.models.signals import post_save, post_delete
from django.conf import settings
import notification

from subscription.signals import recured
from subscription.models import UserSubscription
from muaccounts.models import MUAccount

from django_counter.models import ViewCounter

MUACCOUNT_CT_NAME = 'mu account'

def handle_notify(instance, created, **kwargs):
    if created or instance.content_type.name != MUACCOUNT_CT_NAME \
    or instance.object.owner is None:
        return
    
    if instance.count + settings.GRACE_PAGE_VIEW == instance.object.owner.quotas.page_views:
        notification.models.send([instance.object.owner], 'page_view_quotas_almost_ends', 
                {'muaccount': instance.object, 'residuary_views':settings.GRACE_PAGE_VIEW})
    elif instance.count == instance.object.owner.quotas.page_views:
        notification.models.send([instance.object.owner], 'page_view_quotas_ends', {'muaccount': instance.object})
    elif instance.count == instance.object.owner.quotas.page_views + settings.GRACE_PAGE_VIEW:
        notification.models.send([instance.object.owner], 'account_suspended_page_view_quotas_ends', 
                                 {'muaccount': instance.object})
post_save.connect(handle_notify, sender=ViewCounter)


def flush(sender, **kwargs):
    ViewCounter.objects.filter(object_id__in=sender.user.owned_sites.values_list('id', flat=True),
                               content_type__name=MUACCOUNT_CT_NAME,
                               ).update(count=0)
recured.connect(flush, sender=UserSubscription)

def cleanup(instance, **kwargs):
    counter = ViewCounter.objects.get_for_object(instance)
    counter.delete()
post_delete.connect(cleanup, sender=MUAccount)
