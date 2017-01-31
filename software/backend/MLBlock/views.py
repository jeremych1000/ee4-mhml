from django.shortcuts import render, redirect
from MLBlock.form import FileForm
from django.conf import settings
from MLBlock.models import RawAccData, RawGSRData, RawHRData, RawTempData
from datetime import datetime
import os
import csv


def check_duplicate(name):
    return os.path.isfile(os.path.join(settings.MEDIA_ROOT, name))


def read_raw_file(f, classHandle, datestring):
    obj = classHandle.objects.get(file__contains=datestring)
    fHandle=open(obj.file.path)
    reader = csv.reader(fHandle)
    date_format_string = '%d.%m.%y %H:%M:%S'
    n_param = len(reader.__next__())
    data = [[]] * n_param
    for row in reader:
        data[0].append(datetime.strptime(row[0][0:len(row[0]) - 4], date_format_string))
        for i in range(1, n_param):
            data[i].append()
    fHandle.close()


def upload(request):
    if request.method == 'POST':
        f_form = FileForm(request.POST, request.FILES)
        if f_form.is_valid():
            name = request.FILES['file'].name
            print(os.path.join(settings.MEDIA_ROOT, name))
            print(os.path.isfile(os.path.join(settings.MEDIA_ROOT, name)))
            if not (check_duplicate(name, RawHRData) or check_duplicate(name, RawAccData) or check_duplicate(name,
                                                                                                             RawTempData) or check_duplicate(
                name, RawGSRData)):
                if name.find('Acc') > -1:
                    obj = RawAccData(file=request.FILES['file'])
                    obj.save()
                if name.find('GSR') > -1:
                    obj = RawGSRData(file=request.FILES['file'])
                    obj.save()
                if name.find('HR') > -1:
                    obj = RawHRData(file=request.FILES['file'])
                    obj.save()
                if name.find('Temp') > -1:
                    obj = RawTempData(file=request.FILES['file'])
                    obj.save()

        return redirect('/ml/success/')


def home(request):
    return render(request, 'ml_homepage.html', {'fileForm': FileForm()})


def success(request):
    return render(request, 'success.html',
                  {'acc_count': RawAccData.objects.count(), 'gsr_count': RawGSRData.objects.count(),
                   'temp_count': RawTempData.objects.count(), 'hr_count': RawHRData.objects.count()})
