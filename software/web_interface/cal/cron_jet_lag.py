from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from django_cron import CronJobBase, Schedule

from .models import calendar_events

class SendSleepNotifications(CronJobBase):
    RUN_EVERY_MINS = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cal.send_sleep_notifications'    # a unique code

    def do(self):




        pass