from django.contrib.auth.models import Group

import notification.models
import registration.signals

import muaccounts.signals
import subscription.signals


def handle_user_registered(sender, user, **kwargs):
    group, created = Group.objects.get_or_create(name="Registered Member")
    user.groups.add(group)
    notification.models.send([user], 'welcome')
registration.signals.user_registered.connect(handle_user_registered)

def handle_add_member(sender, user, **kwargs):
    notification.models.send([user], 'member_add', {'muaccount':sender})
muaccounts.signals.add_member.connect(handle_add_member)

def handle_remove_member(sender, user, **kwargs):
    notification.models.send([user], 'member_remove', {'muaccount':sender})
muaccounts.signals.remove_member.connect(handle_remove_member)

def impossible_downgrade(sender, subscription, **kwargs):
    before = sender.subscription
    after = subscription
    if not after.price:
        if before.price: return "You cannot downgrade to a free plan."
        else: return None
    if before.recurrence_unit:
        if not after.recurrence_unit:
            return "You cannot downgrade from recurring subscription to one-time."
        else:
            if after.price_per_day() > before.price_per_day(): return None
            else: return "You cannot downgrade to a cheaper plan."
    else:
        if not after.recurrence_unit:
            if after.price > before.price: return None
            else: return "You cannot downgrade to a cheaper plan."
subscription.signals.change_check.connect(impossible_downgrade)
