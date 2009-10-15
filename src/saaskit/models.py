from django.db import models
from django.contrib.auth.models import User
import signal_handlers


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    real_name = models.CharField(max_length=100)
    about = models.TextField(blank=True)

    website = models.URLField('Website/Blog', verify_exists=False, blank=True)
    company_url = models.URLField(verify_exists=False, blank=True)
    location = models.CharField(max_length=100, blank=True)

    is_public = models.BooleanField()

    @models.permalink
    def get_absolute_url(self):
        return ('profiles_profile_detail',
                (), { 'username': self.user.username })
