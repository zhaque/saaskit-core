from django.contrib.auth.models import User, Group
from django.db import models
from django.utils.safestring import SafeUnicode

import notification.models

import django_pipes as pipes
import mashup.pipeadmin

# handle user registration
from registration.signals import user_registered
def handle_user_registered(sender, user, **kwargs):
    group, created = Group.objects.get_or_create(name="Registered users")
    user.groups.add(group)
    notification.models.send([user], 'welcome')
user_registered.connect(handle_user_registered)

import muaccounts.signals
def handle_add_member(sender, user, **kwargs):
    notification.models.send([user], 'member_add', {'muaccount':sender})
muaccounts.signals.add_member.connect(handle_add_member)

def handle_remove_member(sender, user, **kwargs):
    notification.models.send([user], 'member_remove', {'muaccount':sender})
muaccounts.signals.remove_member.connect(handle_remove_member)

# user profile
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    real_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    # ...

    @models.permalink
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })

# pipes for mashup
class TwitterSearch(pipes.Pipe):
    uri = "http://search.twitter.com/search.json"
    parameters = { 'q' : None,
                   'lang' : None,
                   'rpp' : None,
                   'since_id' : None,
                   'geocode' : None
                   }
    name = 'Twitter Search'
    cache_expiry = 15

    def render(self):
        rv = ['<ul>']
        for result in self.results:
            rv.append(u'<li lang="%s"><img src="%s">%s: %s</li>' % (
                result.iso_language_code,
                result.profile_image_url,
                result.from_user,
                result.text ) )
        rv.append('</ul>')
        return SafeUnicode(u''.join(rv))
mashup.pipeadmin.register(TwitterSearch)

class GoogleSearch(pipes.Pipe):
    uri = "http://ajax.googleapis.com/ajax/services/search/web"
    parameters = { 'q' : None,
                   }
    name = 'Google Search'
mashup.pipeadmin.register(GoogleSearch)
