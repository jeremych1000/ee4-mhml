from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^getrandom/$', views.random_number.as_view(), name='random_api'),
    url(r'raw_data/$', views.raw_data.as_view(), name='raw_data'),
]
