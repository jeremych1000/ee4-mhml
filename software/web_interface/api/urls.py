from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views, graphs
from newML import SetupTesting

urlpatterns = [
    # index
    url(r'^$', RedirectView.as_view(url='/docs/api', permanent=False), name='index'),

    # REST Functions
    url(r'^get_random/$', views.random_number.as_view(), name='random_api'),
    url(r'^on_off/$', views.on_off.as_view(), name='on_off'),
    url(r'^raw_data/$', views.raw_data.as_view(), name='raw_data'),
    url(r'^make_coffee/$', views.teapot.as_view()),

    # data visualisations
    url(r'^stats/heartrate/last/(?P<days>\d+)/graph/$', graphs.heartrate),
    url(r'^stats/heartrate/last/(?P<days>\d+)/$', views.stats.heartrate.last.as_view()),
    #url(r'^stats/heartrate/from//to/$'),

    url(r'^stats/rr/last/(?P<days>\d+)/graph/$', graphs.rr),
    url(r'^stats/rr/last/(?P<days>\d+)/$', views.stats.rr.last.as_view()),
    #url(r'^stats/rr/from//to/$'),

    url(r'^stats/gsr/last/(?P<days>\d+)/graph/$', graphs.gsr),
    url(r'^stats/gsr/last/(?P<days>\d+)/$', views.stats.gsr.last.as_view()),
    #url(r'^stats/gsr/from//to/$'),

    url(r'^stats/temperature/last/(?P<days>\d+)/graph/$', graphs.temperature),
    url(r'^stats/temperature/last/(?P<days>\d+)/$', views.stats.temperature.last.as_view()),
    #url(r'^stats/temperature/from//to/$'),

    url(r'^stats/acceleration/last/(?P<days>\d+)/graph/$', graphs.acceleration),
    url(r'^stats/acceleration/last/(?P<days>\d+)/$', views.stats.acceleration.last.as_view()),
    #url(r'^stats/acceleration/from//to/$'),


    url(r'rt/$', views.realTimeResponse.as_view(), name='rt'),
    url(r'uf/$', views.userFeedback.as_view(), name='uf'),

    url(r'^stats/random/$', graphs.initial_test),

    # non REST functions
    url(r'make_default/$', SetupTesting.settingDefault),
    url(r'migrate_feature/$', SetupTesting.migrateFeature),
]