"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from lists import views as list_views
from MLBlock import views as ml_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', ml_views.home, name='ml_home'),
    url(r'^ml/$', ml_views.home, name='ml_home'),
    url(r'^lists/$', list_views.home_page, name='list_home'),
    url(r'^lists/new/$', list_views.new_list, name='new_list'),
    url(r'^lists/(?P<list_id>\d+)/items/new/$', list_views.new_item, name='new_item'),
    url(r'^lists/(\d+)/$', list_views.view_list, name='view_list'),
    url(r'^lists/(?P<listID>\d+)/delete/(?P<itemID>\d+)/$', list_views.delete_item, name='delete_item'),
    url(r'^lists/(?P<listID>\d+)/delete/$', list_views.delete_list, name='delete_list'),
    url(r'^ml/upload/$', ml_views.upload, name='ml_file_upload'),
    url(r'^ml/success/$', ml_views.success, name='ml_success'),
]
