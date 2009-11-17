### -*- coding: utf-8 -*- ####################################################

from django.db.models.signals import post_save, post_delete
from django.conf import settings

from subscription.models import UserSubscription

def delete_accounts(instance, **kwargs):
    instance.user.owned_sites.all().delete()
post_delete.connect(delete_accounts, sender=UserSubscription)
