from django.contrib import admin
from accounts.models import UserProfile, TestPost

admin.site.register(UserProfile)
admin.site.register(TestPost)
