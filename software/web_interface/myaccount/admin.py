from django.contrib import admin
from myaccount.models import UserProfile, TestPost

admin.site.register(UserProfile)
admin.site.register(TestPost)
