from django.contrib.auth.models import User
from django.utils import timezone

from datetime import datetime, date, timedelta

from newML.models import FeatureEntry
from newML import functions


def live_data(request):
    user_object = User.objects.get(username="jeremych")

    today = timezone.now()
    start_date = today - timedelta(0.1)

    last_data = FeatureEntry.objects.all().filter(user=user_object, date__gte=start_date)
    if len(last_data) != 0:
        last_data = last_data.latest('date')
        mean_hr = int(last_data.mean_hr)
        mean_rr = round(last_data.mean_rr, 2)
        mean_gsr = round(last_data.mean_gsr, 2)
        mean_temp = int(last_data.mean_temp)
        mean_acc = round(last_data.mean_acc, 2)

        # print(mean_hr, mean_rr, mean_gsr, mean_temp, mean_acc)

    return {
        "current_user": user_object.username,
        "mean_hr": {
            "current": mean_hr,
            "min": 0,
            "max": 200,
            "width": int(100 * mean_hr / 200),
        },
        "mean_rr": {
            "current": int(100 * mean_rr),
            "min": 0,
            "max": 100 * 1,
            "width": int(100 * mean_rr),
        },
        "mean_gsr": {
            "current": int(mean_gsr),
            "min": 1000,
            "max": 20000,
            "width": int(100 * mean_gsr / 20000),
        },
        "mean_temp": {
            "current": mean_temp,
            "min": 0,
            "max": 100,
            "width": int(100 * mean_temp / 100),
        },
        "mean_acc": {
            "current": int(100 * mean_acc),
            "min": 0,
            "max": 100 * 1,
            "width": int(100 * mean_acc),
        },
    }
