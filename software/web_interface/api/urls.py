from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views
from newML import SetupTesting

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/docs/api', permanent=False), name='index'),
    url(r'^get_random/$', views.random_number.as_view(), name='random_api'),
    url(r'^on_off/$', views.on_off.as_view(), name='on_off'),
    url(r'raw_data/$', views.raw_data.as_view(), name='raw_data'),
    url(r'make_coffee/$', views.teapot.as_view()),
    url(r'make_default/$', SetupTesting.settingDefault),
]
