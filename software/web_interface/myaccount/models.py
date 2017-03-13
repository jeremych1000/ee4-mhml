from django.db import models
from django.contrib.auth.models import User


# extend django user model
class UserProfile(models.Model):
    # one to one mappiong of user model
    user = models.OneToOneField(User)

    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username


class TestPost(models.Model):
    post_data = models.CharField(max_length=30, blank=True)

class PushyToken(models.Model):
    user = models.OneToOneField(User, unique=True)
    token = models.CharField(max_length=50)

