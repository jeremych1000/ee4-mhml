from django.shortcuts import render, redirect
from MLBlock.form import FileForm
from django.conf import settings
import os


def handle_upload_file(f, name):
    with open(os.path.join(''.join(settings.ML_MEDIA_DIR), name), 'wb+')as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload(request):
    if request.method == 'POST':
        f_form = FileForm(request.POST, request.FILES)
        if f_form.is_valid():
            handle_upload_file(request.FILES['file'], request.FILES['file'].name)
            return redirect('/MLBlock/success/')


def home(request):
    return render(request, 'ml_homepage.html', {'fileForm': FileForm()})
