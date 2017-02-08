from django.shortcuts import render
from django.contrib import messages

def index(request):
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

def logged_in(request, user=None):
    if user.is_authenticated:
        messages.info(request, "authenticated")
    else:
        messages.warning(request, "no")

    return render(request, "personal/home.html", {'user_model': user})