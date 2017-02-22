from django.contrib.auth.models import User

from newML.models import FeatureEntry
from datetime import datetime, date, timedelta
from . import serializers

def get_last_temperature(request, days):
    start_date = datetime.now() + timedelta(-int(days))

    user_object = User.objects.get(username=request.user)
    print(user_object, type(user_object))

    features = FeatureEntry.objects.all().filter(user=user_object, date__gte=start_date)
    print(features, type(features), len(features))

    serializer = serializers.FeatureEntrySerializer(features, many=True)

    return serializer