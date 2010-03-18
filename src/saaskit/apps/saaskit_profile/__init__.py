from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save

import notification.models
import registration.signals

import muaccounts.signals

def set_default_group(user):
    """add default group Registered Member"""
    group, created = Group.objects.get_or_create(name="Registered Member")
    user.groups.add(group)
    notification.models.send([user], 'welcome')

reg_func = lambda user, **kwargs: set_default_group(user)
registration.signals.user_registered.connect(reg_func)

def handle_add_member(sender, user, **kwargs):
    notification.models.send([user], 'member_add', {'muaccount':sender})
muaccounts.signals.add_member.connect(handle_add_member)

def handle_remove_member(sender, user, **kwargs):
    notification.models.send([user], 'member_remove', {'muaccount':sender})
muaccounts.signals.remove_member.connect(handle_remove_member)
