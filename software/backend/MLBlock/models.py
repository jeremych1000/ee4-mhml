from django.db import models


class RawData(models.Model):
    file = models.FileField(null=True, blank=True)


class FileTracker(models.Model):
    accCount = models.IntegerField(default=0)


class FeatureEntries(models.Model):
    date = models.DateTimeField(auto_now_add=True)


class MeanHR(models.Model):
    data = models.FloatField(default=0.0)
    featureEntry = models.ForeignKey('FeatureEntries', on_delete=models.CASCADE)


class StdHR(models.Model):
    data = models.FloatField(default=0.0)
    featureEntry = models.ForeignKey('FeatureEntries', on_delete=models.CASCADE)


class MeanRR(models.Model):
    data = models.FloatField(default=0.0)
    featureEntry = models.ForeignKey('FeatureEntries', on_delete=models.CASCADE)


class StdRR(models.Model):
    data = models.FloatField(default=0.0)
    featureEntry = models.ForeignKey('FeatureEntries', on_delete=models.CASCADE)


class MeanGSR(models.Model):
    data = models.FloatField(default=0.0)
    featureEntry = models.ForeignKey('FeatureEntries', on_delete=models.CASCADE)


class StdGSR(models.Model):
    data = models.FloatField(default=0.0)
    featureEntry = models.ForeignKey('FeatureEntries', on_delete=models.CASCADE)


class MeanTemp(models.Model):
    data = models.FloatField(default=0.0)
    featureEntry = models.ForeignKey('FeatureEntries', on_delete=models.CASCADE)


class StdTemp(models.Model):
    data = models.FloatField(default=0.0)
    featureEntry = models.ForeignKey('FeatureEntries', on_delete=models.CASCADE)


class MeanAcc(models.Model):
    data = models.FloatField(default=0.0)
    featureEntry = models.ForeignKey('FeatureEntries', on_delete=models.CASCADE)
