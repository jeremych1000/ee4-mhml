from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class calendar_link(models.Model):
    user = models.OneToOneField(User, unique=True)
    link = models.URLField()

#class calendar_events(models.Model):
#    # only store user's next day events, have a way to refresh it
#    user = models.OneToOneField(User)
#    event_start = models.DateTimeField()
#    notification_sent = models.BooleanField(default=False)