from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User
import os

# https://docs.djangoproject.com/en/1.10/topics/auth/customizing/#referencing-the-user-model
# Need to link username to actual user account model !!

class FeatureEntry(models.Model):
    AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    mean_hr = models.FloatField(default=0.0)
    std_hr = models.FloatField(default=0.0)
    mean_rr = models.FloatField(default=0.0)
    std_rr = models.FloatField(default=0.0)
    mean_gsr = models.FloatField(default=0.0)
    std_gsr = models.FloatField(default=0.0)
    mean_temp = models.FloatField(default=0.0)
    std_temp = models.FloatField(default=0.0)
    mean_acc = models.FloatField(default=0.0)
    label = models.NullBooleanField(default="", blank=False, null=True)


class ModelFile(models.Model):
    AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
    file = models.FileField(null=True, blank=True,
                            storage=FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'model')))
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    untrained = models.IntegerField(default=0)
