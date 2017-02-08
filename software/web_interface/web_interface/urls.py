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
from accounts.forms import LoginForm

#for static media
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^', include("personal.urls"), name='home'),

    #login stuff
    #url(r'^accounts/login/$', views.login),
    #url(r'^accounts/auth/$', views.auth_view),
    #url(r'^accounts/logout/$', views.logout),
    #url(r'^accounts/loggedin/$', views.loggedin),
    #url(r'^accounts/invalid/$', views.invalid_login),

    url(r'^accounts/', include('accounts.urls')),
    #url(r'accounts/login/$', views.login, {'template_name': 'accounts/login.html', 'authentication_form': LoginForm}, name='login'),
    #url(r'accounts/logout/$', views.logout, {'next_page': '/'}, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)