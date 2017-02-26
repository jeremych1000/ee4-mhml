from django.contrib.auth.models import User

from newML.models import FeatureEntry
from datetime import datetime, date, timedelta
from django.utils import timezone
from . import serializers

def last_days(request, days):
    start_date = timezone.now() + timedelta(-int(days))
    user_object = User.objects.get(username="jeremych")
    features = FeatureEntry.objects.all().filter(user=user_object, date__gte=start_date)
    return features


def heartrate(request, days):
    features = last_days(request=request, days=days)
    serializer = serializers.FeatureEntrySerializer.heartrate(features, many=True)
    return serializer

def rr(request, days):
    features = last_days(request=request, days=days)
    serializer = serializers.FeatureEntrySerializer.rr(features, many=True)
    return serializer

def gsr(request, days):
    features = last_days(request=request, days=days)
    serializer = serializers.FeatureEntrySerializer.gsr(features, many=True)
    return serializer

def temperature(request, days):
    features = last_days(request=request, days=days)
    serializer = serializers.FeatureEntrySerializer.temperature(features, many=True)
    return serializer

def acceleration(request, days):
    features = last_days(request=request, days=days)
    serializer = serializers.FeatureEntrySerializer.acceleration(features, many=True)
    return serializer