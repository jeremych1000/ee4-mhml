from django.shortcuts import render

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