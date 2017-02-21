from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
# TODO: combine all feature models into one large database with username timestamp data
# create sleepquality model with start time, stop time, username, sleep quality (good/bad)
# so use sleepquality models start/stop to filter large database entries
# https://docs.djangoproject.com/en/1.10/topics/db/models/#automatic-primary-key-fields
# after training, update model with largest trained ID
# hook on upon new entry to model

class RawData(models.Model):
    file = models.FileField(null=True, blank=True,
                            storage=FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'data')))
    username = models.CharField(max_length=50)


class FileTracker(models.Model):
    accCount = models.IntegerField(default=0)
    username = models.CharField(max_length=50)


class FeatureEntries(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=50)


class MeanHR(models.Model):
    data = models.FloatField(default=0.0)
    featureEntry = models.ForeignKey('FeatureEntries', on_delete=models.CASCADE)
    username = models.ForeignKey('FeatureEntries', related_name='%(class)s_username')


class StdHR(models.Model):
    data = models.FloatField(default=0.0)
    featureEntry = models.ForeignKey('FeatureEntries', on_delete=models.CASCADE)
    username = models.ForeignKey('FeatureEntries', related_name='%(class)s_username')


class MeanRR(models.Model):
    data = models.FloatField(default=0.0)
    featureEntry = models.ForeignKey('FeatureEntries', on_delete=models.CASCADE)
    username = models.ForeignKey('FeatureEntries', related_name='%(class)s_username')


class StdRR(models.Model):
    data = models.FloatField(default=0.0)
    featureEntry = models.ForeignKey('FeatureEntries', on_delete=models.CASCADE)
    username = models.ForeignKey('FeatureEntries', related_name='%(class)s_username')


class MeanGSR(models.Model):
    data = models.FloatField(default=0.0)
    featureEntry = models.ForeignKey('FeatureEntries', on_delete=models.CASCADE)
    username = models.ForeignKey('FeatureEntries', related_name='%(class)s_username')


class StdGSR(models.Model):
    data = models.FloatField(default=0.0)
    featureEntry = models.ForeignKey('FeatureEntries', on_delete=models.CASCADE)
    username = models.ForeignKey('FeatureEntries', related_name='%(class)s_username')


class MeanTemp(models.Model):
    data = models.FloatField(default=0.0)
    featureEntry = models.ForeignKey('FeatureEntries', on_delete=models.CASCADE)
    username = models.ForeignKey('FeatureEntries', related_name='%(class)s_username')


class StdTemp(models.Model):
    data = models.FloatField(default=0.0)
    featureEntry = models.ForeignKey('FeatureEntries', on_delete=models.CASCADE)
    username = models.ForeignKey('FeatureEntries', related_name='%(class)s_username')


class MeanAcc(models.Model):
    data = models.FloatField(default=0.0)
    featureEntry = models.ForeignKey('FeatureEntries', on_delete=models.CASCADE)
    username = models.ForeignKey('FeatureEntries', related_name='%(class)s_username')


class SleepQuality(models.Model):
    data = models.BooleanField(default=False)
    featureEntry = models.ForeignKey('FeatureEntries', on_delete=models.CASCADE)
    username = models.ForeignKey('FeatureEntries', related_name='%(class)s_username')
