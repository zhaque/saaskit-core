from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    real_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    # ...

    @models.permalink
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
