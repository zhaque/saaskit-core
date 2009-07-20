from django.contrib.auth.models import Group

import notification.models
from registration.signals import user_registered

import muaccounts.signals

def handle_user_registered(sender, user, **kwargs):
    group, created = Group.objects.get_or_create(name="Registered Member")
    user.groups.add(group)
    notification.models.send([user], 'welcome')
user_registered.connect(handle_user_registered)

def handle_add_member(sender, user, **kwargs):
    notification.models.send([user], 'member_add', {'muaccount':sender})
muaccounts.signals.add_member.connect(handle_add_member)

def handle_remove_member(sender, user, **kwargs):
    notification.models.send([user], 'member_remove', {'muaccount':sender})
muaccounts.signals.remove_member.connect(handle_remove_member)
