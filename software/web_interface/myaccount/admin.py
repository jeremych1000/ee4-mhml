from django.contrib import admin
from myaccount.models import UserProfile, TestPost, PushyToken

admin.site.register(UserProfile)
admin.site.register(TestPost)
admin.site.register(PushyToken)
