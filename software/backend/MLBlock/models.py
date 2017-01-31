from django.db import models


class RawAccData(models.Model):
    # time = models.DateTimeField()
    # X = models.FloatField()
    # Y = models.FloatField()
    # Z = models.FloatField()
    file = models.FileField(null=True, blank=True)


class RawTempData(models.Model):
    # time = models.DateTimeField()
    # temp = models.FloatField()
    file = models.FileField(null=True, blank=True)


class RawGSRData(models.Model):
    # time = models.DateTimeField(null=True, blank=True)
    # gsr = models.FloatField()
    file = models.FileField(null=True, blank=True)


class RawHRData(models.Model):
    # time = models.DateTimeField()
    # hr = models.FloatField()
    # rr = models.FloatField()
    # mode = models.TextField()
    file = models.FileField(null=True, blank=True)
