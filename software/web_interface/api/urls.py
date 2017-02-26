from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from . import views, graphs
from newML import SetupTesting
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    # index
    url(r'^$', RedirectView.as_view(url='/docs/api', permanent=False), name='index'),

    # rest token JWT auth
    url(r'^auth/token/$', obtain_jwt_token),
    # rest auth
    url(r'^auth/registration/', include('rest_auth.registration.urls')),
    url(r'^auth/', include('rest_auth.urls')),

    # REST Functions
    url(r'^get_random/$', views.random_number.as_view(), name='random_api'),
    url(r'^on_off/$', views.on_off.as_view(), name='on_off'),
    url(r'^raw_data/$', views.raw_data.as_view(), name='raw_data'),
    url(r'^make_coffee/$', views.teapot.as_view()),

    # data visualisations
    url(r'^stats/last/(?P<days>\d+)/(?P<feature>[a-z_]+)/$', views.stats.last.as_view()),
    url(r'^stats/last/(?P<days>\d+)/(?P<feature>[a-z_]+)/graph/$', graphs.simple_graph),
    url(r'^stats/from/(?P<start>[0-9:\-T]+)/to/(?P<end>[0-9:\-T]+)/(?P<feature>[a-z_]+)/$', views.stats.date_range.as_view()),

    url(r'^rt/$', views.realTimeResponse.as_view(), name='rt'),
    url(r'^uf/$', views.userFeedback.as_view(), name='uf'),

    url(r'^stats/random/$', graphs.initial_test),

    # non REST functions`
    url(r'^make_default/$', SetupTesting.settingDefault),
    url(r'^migrate_feature/$', SetupTesting.migrateFeature),
]