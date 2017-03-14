from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class calendar_link(models.Model):
    user = models.OneToOneField(User, unique=True)
    link = models.URLField()

class calendar_events(models.Model):
    # only store user's next day events, have a way to refresh it
    user = models.ForeignKey(User)
    event_summary = models.CharField(max_length=50)
    event_start = models.DateTimeField()
    event_tz = models.CharField(max_length=20)
    notification_sent = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'event_summary', 'event_start')