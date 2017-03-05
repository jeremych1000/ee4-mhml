from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^about/$', views.about, name='about'),
    url(r'^download/$', views.download, name='download'),
    url(r'^privacy/$', views.privacy, name='privacy'),
    url(r'^log/$', views.log, name='log'),
    url(r'^blank/$', views.blank),
]
