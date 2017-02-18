from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='ml_home'),
    url(r'^upload/$', views.upload, name='ml_file_upload'),
    url(r'post/$', views.add_raw_data, name='ml_post'),
]
