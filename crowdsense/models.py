from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import SafeUnicode

import django_pipes as pipes
import mashup.pipeadmin

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
