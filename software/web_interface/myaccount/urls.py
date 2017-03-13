from django.conf.urls import url
from . import views

urlpatterns = [
    # need to deprecate for allauth
    # url(r'^register/$', views.register, name='register'),
    # url(r'^login/$', views.user_login, name='login'),
    # url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^$', views.profile, name='index'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^calendar/add/$', views.calendar_add, name='calendar'),
    url(r'^calendar/$', views.calendar, name='calendar'),
    url(r'^statistics/$', views.stats, name='stats'),

    url(r'^testpost/$', views.test_post),
    url(r'dl/$', views.dl),
]
