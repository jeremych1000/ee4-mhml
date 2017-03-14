# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from .models import calendar_link

from icalendar import Calendar
from icalendar import vDatetime, vText
import datetime, requests, json

"""
    %a  Locale’s abbreviated weekday name.
    %A  Locale’s full weekday name.
    %b  Locale’s abbreviated month name.
    %B  Locale’s full month name.
    %c  Locale’s appropriate date and time representation.
    %d  Day of the month as a decimal number [01,31].
    %f  Microsecond as a decimal number [0,999999], zero-padded on the left
    %H  Hour (24-hour clock) as a decimal number [00,23].
    %I  Hour (12-hour clock) as a decimal number [01,12].
    %j  Day of the year as a decimal number [001,366].
    %m  Month as a decimal number [01,12].
    %M  Minute as a decimal number [00,59].
    %p  Locale’s equivalent of either AM or PM.
    %S  Second as a decimal number [00,61].
    %U  Week number of the year (Sunday as the first day of the week)
    %w  Weekday as a decimal number [0(Sunday),6].
    %W  Week number of the year (Monday as the first day of the week)
    %x  Locale’s appropriate date representation.
    %X  Locale’s appropriate time representation.
    %y  Year without century as a decimal number [00,99].
    %Y  Year with century as a decimal number.
    %z  UTC offset in the form +HHMM or -HHMM.
    %Z  Time zone name (empty string if the object is naive).
    %%  A literal '%' character.
"""


def get_cal_events(username=None):
    if username is not None:
        cal_events = []
        user = User.objects.get(username=username)
        cal_link = calendar_link.objects.get(user=user).link

        file = requests.get(url=cal_link)
        cal = Calendar.from_ical(file.content)

        for component in cal.walk():
            cal_event_temp = {}
            if 'summary' in component and 'dtstart' in component and 'dtend' in component:
                if component.name == "VEVENT":
                    summary = component.get('summary')
                    summary = vText.from_ical(summary)
                    # print(summary, type(summary))
                    if summary is not None:
                        cal_event_temp["summary"] = summary
                        # print(summary)
                    else:
                        raise

                    start = component.get('dtstart').dt
                    if start is not None:
                        cal_event_temp["start"] = start.strftime("%d/%m/%y %H:%M:%S %z")
                        # print(start, type(start))
                        # print(start.year, start.month, start.day)
                    else:
                        raise

                    end = component.get('dtend').dt
                    if end is not None:
                        cal_event_temp["end"] = end.strftime("%d/%m/%y %H:%M:%S %z")
                        # print(end, type(end))
                    else:
                        raise

                    if start is not None and end is not None:
                        pass
                        # print(end - start)
                cal_events.append(cal_event_temp)
                # print(cal_events)

                # print(cal_events, type(cal_events))
        return {"data": cal_events}
    else:
        return {}
