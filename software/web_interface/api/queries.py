from django.contrib.auth.models import User

from newML.models import FeatureEntry
from datetime import datetime, date, timedelta
from django.utils import timezone
from . import serializers

def last_days(request, days):
    start_date = timezone.now() - timedelta(days=int(days))
    user_object = User.objects.get(username=request.user.username)
    features = FeatureEntry.objects.all().filter(user=user_object, date__gte=start_date)
    return features


def heartrate(request, days):
    features = last_days(request=request, days=days)
    serializer = serializers.FeatureEntrySerializer.mean_hr(features, many=True)
    return serializer

def rr(request, days):
    features = last_days(request=request, days=days)
    serializer = serializers.FeatureEntrySerializer.mean_rr(features, many=True)
    return serializer

def gsr(request, days):
    features = last_days(request=request, days=days)
    serializer = serializers.FeatureEntrySerializer.mean_gsr(features, many=True)
    return serializer

def temperature(request, days):
    features = last_days(request=request, days=days)
    serializer = serializers.FeatureEntrySerializer.mean_temp(features, many=True)
    return serializer

def acceleration(request, days):
    features = last_days(request=request, days=days)
    serializer = serializers.FeatureEntrySerializer.mean_acc(features, many=True)
    return serializer