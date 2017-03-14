from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.db import IntegrityError

from .models import calendar_link, calendar_events
from .read import get_cal_events

from icalendar import Calendar
from icalendar import vDatetime, vText
import datetime, requests, json, pytz


def import_all(days=3):
    calendar_link_obj = calendar_link.objects.all()
    timedelta = datetime.timedelta(days=days)
    time_now = timezone.now()

    date_cutoff = time_now + timedelta
    # print(date_cutoff, type(date_cutoff), date_cutoff.tzinfo, timezone.now(), timedelta)

    exception_list = []
    for i in calendar_link_obj:
        json_cal = get_cal_events(i.user.username)

        for j in json_cal["data"]:
            # ("%d/%m/%y %H:%M:%S %z")
            start = datetime.datetime.strptime(j["start"], "%d/%m/%y %H:%M:%S %z")
            # print(start, type(start), start.tzinfo, type(start.tzinfo))
            if start < date_cutoff and start > time_now:
                try:
                    calendar_events.objects.create(
                        user=i.user,
                        event_summary=j["summary"],
                        event_start=start,
                        event_tz=str(start.tzinfo),
                    )
                except (ValueError, IntegrityError) as e:
                    exception_list.append({"message": str(e), "type": str(type(e))})
    return exception_list
