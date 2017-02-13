from django.shortcuts import render, redirect
from MLBlock.form import FileForm
from django.conf import settings
from MLBlock.models import RawData, FileTracker, FeatureEntries
from datetime import datetime
import MLBlock.FeatureExtraction as fe
import MLBlock.ServerFunction as func
import os
import csv
import re


def check_duplicate(name):
    return os.path.isfile(os.path.join(settings.MEDIA_ROOT, name))


def read_raw_file(classHandle, datestring):
    obj = classHandle.objects.get(file__contains=datestring)
    fHandle = open(obj.file.path)
    reader = csv.reader(fHandle)
    date_format_string = '%d.%m.%y %H:%M:%S'
    n_param = len(reader.__next__())
    data = []
    for i in range(0, n_param):
        data.append([])
    for row in reader:
        data[0].append(datetime.strptime(row[0][0:len(row[0]) - 4], date_format_string))
        # Data Processing
        for i in range(1, n_param):
            data[i].append(row[i])
    fHandle.close()
    return data


def upload(request):
    if request.method == 'POST':
        f_form = FileForm(request.POST, request.FILES)
        if f_form.is_valid():
            name = request.FILES['file'].name
            regexR=re.search(r'(MSBand2_ALL_data_)(\w+)',name)
            data_date = regexR.group(2)
            if not (check_duplicate(name)):
                raw = RawData.objects.create(file=request.FILES['file'])
                db_feautre = FeatureEntries.objects.create(date=datetime.strptime(data_date, '%d_%m_%y'))
                func.InsertFeature2DB(fe.genfeatureFromCSV(raw.file.path, 600), db_feautre)
                if FileTracker.objects.count() == 0:
                    FileTracker.objects.create(accCount=1)
                else:
                    print(FileTracker.objects.count())
                    obj = FileTracker.objects.first()
                    obj.accCount += 1
                    obj.save()
                    if obj.accCount == 20:
                        pass
        return redirect('/ml/success/')


def home(request):
    return render(request, 'ml_homepage.html', {'fileForm': FileForm()})


def success(request):
    return render(request, 'success.html',
                  {'count': RawData.objects.count()})
