from django.shortcuts import render
from django.contrib import messages

import requests

def index(request):
    if request.method == 'GET' and 'action' in request.GET:
        if request.GET['action'] == "login":
            return render(request, "personal/home.html", {'login': True})
    else:
        if request.user.is_authenticated():
            a = requests.get('http://sleepify.zapto.org/api/stats/temperature/last/3/graph/')
            print(a, type(a))
            pass
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


def blank(request):
    return render(request, "personal/blank.html")
