from django.contrib import admin
from . import models

admin.site.register(models.calendar_link)
admin.site.register(models.calendar_events)