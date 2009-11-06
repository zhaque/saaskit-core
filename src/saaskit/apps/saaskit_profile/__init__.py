from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save

import notification.models
import registration.signals

import muaccounts.signals

def user_registered(instance, created, **kwargs):
    if created:
        group, created = Group.objects.get_or_create(name="Registered Member")
        instance.groups.add(group)
        notification.models.send([instance], 'welcome')
post_save.connect(user_registered, sender=User)

def handle_add_member(sender, user, **kwargs):
    notification.models.send([user], 'member_add', {'muaccount':sender})
muaccounts.signals.add_member.connect(handle_add_member)

def handle_remove_member(sender, user, **kwargs):
    notification.models.send([user], 'member_remove', {'muaccount':sender})
muaccounts.signals.remove_member.connect(handle_remove_member)
