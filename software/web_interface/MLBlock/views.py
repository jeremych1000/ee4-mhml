from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from MLBlock.models import RawData, FileTracker, FeatureEntries
from MLBlock.form import FileForm
import MLBlock.FeatureExtraction as fe
import MLBlock.ServerFunction as func

from datetime import datetime
from collections import deque
import os, csv, re, json

#file_prefix = "MSBand2_ALL_data_"


def check_duplicate(name, username=None):
    if username is None:
        path = os.path.join(os.path.join(settings.MEDIA_ROOT, 'data'), name)
    else:
        path = os.path.join(os.path.join(os.path.join(settings.MEDIA_ROOT, 'data'), username), name)
    #print("check duplidate Path is ", path)
    return os.path.isfile(path)


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
    uploaded = False

    username = "test"

    if request.method == 'POST':
        f_form = FileForm(request.POST, request.FILES)

        if f_form.is_valid() and len(request.FILES) != 0:
            name = request.FILES['file'].name
            regexR = re.search(r'(MSBand2_ALL_data_)(\w+)', name)
            print(name, regexR)
            data_date = regexR.group(2)
            if not (check_duplicate(name)):
                raw = RawData.objects.create(file=request.FILES['file'])
                db_feature = FeatureEntries.objects.create(date=datetime.strptime(data_date, '%d_%m_%y'))
                func.InsertFeature2DB(fe.genfeatureFromCSV(raw.file.path, 600), db_feature, username)
                if FileTracker.objects.count() == 0:
                    FileTracker.objects.create(accCount=1, username=username)
                else:
                    # print(FileTracker.objects.count())
                    obj = FileTracker.objects.first()
                    obj.accCount += 1
                    obj.save()
                    uploaded = True
                    print("A file has been uploaded to /media/data.")
                    if obj.accCount == 20:
                        # TODO: add machine learning stuff here
                        pass
            else:
                print("A duplicate has been detected, not uploaded.")
        else:
            print(f_form.errors)
            print(f_form.non_field_errors)
    return render(request, "ml/ml_homepage.html", {'uploaded': uploaded,
                                                   'count': RawData.objects.count(),
                                                   })


#def raw_data(request) moved to /api/raw_data

def home(request):
    return render(request, "ml/ml_homepage.html", {'uploaded': False,
                                                   'fileForm': FileForm()})
