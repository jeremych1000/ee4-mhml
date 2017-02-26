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
    url(r'^stats/last/(?P<feature>[a-z]+)/(?P<days>\d+)/$', views.stats.last.as_view()),
    url(r'^stats/last/(?P<feature>[a-z]+)/(?P<days>\d+)/graph/$', graphs.simple_graph),
    url(r'^stats/from/(?P<start>[0-9:\-T]+)/to/(?P<end>[0-9:\-T]+)/(?P<feature>[a-z]+)/$', views.stats.date_range.as_view()),

    url(r'rt/$', views.realTimeResponse.as_view(), name='rt'),
    url(r'uf/$', views.userFeedback.as_view(), name='uf'),

    url(r'^stats/random/$', graphs.initial_test),

    # non REST functions`
    url(r'make_default/$', SetupTesting.settingDefault),
    url(r'migrate_feature/$', SetupTesting.migrateFeature),
]