from django.contrib.auth.models import User

from .models import calendar_link

from icalendar import Calendar
import datetime, requests

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

username = 'jeremych'
print("31231123123122)")
user_object = User.objects.get(username=username)
print("312312)")
cal_link = calendar_link.objects.get(user=user_object)

# download user ics file
url = cal_link.link

file = requests.get(url=url)
gcal = Calendar.from_ical(file.content)

for component in gcal.walk():
    if component.name == "VEVENT":
        summary = component.get('summary')
        if summary is not None:
            print(summary)
        else:
            raise

        start = component.get('dtstart').dt
        if start is not None:
            print(start, type(start))
            print(start.year, start.month, start.day)
        else:
            raise

        end = component.get('dtend').dt
        if end is not None:
            print(end, type(end))
        else:
            raise

        if start is not None and end is not None:
            print(end - start)

# <bound method CaselessDict.get of VEVENT({'DTSTART': <icalendar.prop.vDDDTypes object at 0x000001C71290EB00>, 'DTSTAMP': <icalendar.prop.vDDDTypes object at 0x000001C71290E630>, 'SUMMARY': vText('b'CUHK interview''), 'SEQUENCE': 0, 'TRANSP': vText('b'OPAQUE''), 'UID': vText('b'2479705h0rfgeohn278m3g3s2o@google.com''), 'DESCRIPTION': vText('b'''), 'LAST-MODIFIED': <icalendar.prop.vDDDTypes object at 0x000001C71290ECC0>, 'LOCATION': vText('b'''), 'DTEND': <icalendar.prop.vDDDTypes object at 0x000001C71290EB38>, 'CREATED': <icalendar.prop.vDDDTypes object at 0x000001C71290EC50>, 'STATUS': vText('b'CONFIRMED'')})>
