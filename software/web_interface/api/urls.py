from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^random/$', views.random_outcome, name='random'),
    url(r'^getrandom/$', views.random_api.as_view(), name='random_api'),
]
