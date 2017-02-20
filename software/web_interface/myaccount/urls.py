from django.conf.urls import url
from . import views

urlpatterns = [
    #need to deprecate for allauth
    #url(r'^register/$', views.register, name='register'),
    #url(r'^login/$', views.user_login, name='login'),
    #url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^$', views.profile, name='index'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^preferences/$', views.preferences, name='preferences'),

    url(r'^testpost/$', views.test_post),
    url(r'dl/$', views.dl),
]