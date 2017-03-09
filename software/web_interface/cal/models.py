from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class calendar_link(models.Model):
    user = models.OneToOneField(User)
    link = models.URLField()
