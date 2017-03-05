from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse

import requests, os

def index(request):
    if request.method == 'GET' and 'action' in request.GET:
        if request.GET['action'] == "login":
            return render(request, "personal/home.html", {'login': True})
    else:
        if request.user.is_authenticated():
            return render(request, "personal/home.html")
        else:
            return render(request, "personal/home.html")


def contact(request):
    details = [
        {'name': 'Jeremy Chan', 'email': 'jc4913@ic.ac.uk'},
        {'name': 'Tsz Ho Ho', 'email': 'thh13@ic.ac.uk'},
        {'name': 'Dominic Kwok', 'email': 'cyk113@ic.ac.uk'},
        {'name': 'Ho Shun Lo', 'email': 'hsl113@ic.ac.uk'},
        {'name': 'Nathalie Wong', 'email': 'nw813@ic.ac.uk'},
    ]
    return render(request, "personal/contact.html", {'details': details})


def about(request):
    return render(request, "personal/about.html")


def download(request):
    return render(request, "personal/download.html")

def privacy(request):
    return render(request, "personal/privacy.html")

@login_required
def log(request):
    path = os.path.join(settings.STATICFILES_DIRS[0], 'log.log')
    # print(path)
    with open(path, 'r') as myfile:
        data=myfile.read()
    return HttpResponse(data, content_type='text/plain')

def blank(request):
    return render(request, "personal/blank.html")

