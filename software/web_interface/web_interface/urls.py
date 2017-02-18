"""web_interface URL Configuration

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

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views

#for static media
from django.conf import settings
from django.conf.urls.static import static

#self
from MLBlock import views as ml_views

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),

    url(r'^', include("personal.urls"), name='home'),

    url(r'^myaccount/', include('myaccount.urls'), name='myaccount'),
    url(r'^accounts/', include('allauth.urls'), name='allauth'),
    url(r'^ml/', include('MLBlock.urls'), name='ml'),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)