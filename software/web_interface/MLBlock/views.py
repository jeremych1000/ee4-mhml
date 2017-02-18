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

file_prefix = "MSBand2_ALL_data_"

def check_duplicate(name, username=None):
    if username is None:
        path = os.path.join(os.path.join(settings.MEDIA_ROOT, 'data'), name)
    else:
        path = os.path.join(os.path.join(os.path.join(settings.MEDIA_ROOT, 'data'), username), name)
    print("Path is ", path)
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
    if request.method == 'POST':
        f_form = FileForm(request.POST, request.FILES)

        if f_form.is_valid() and len(request.FILES) != 0:
            name = request.FILES['file'].name
            regexR=re.search(r'(file_prefix)(\w+)',name)
            data_date = regexR.group(2)
            if not (check_duplicate(name)):
                raw = RawData.objects.create(file=request.FILES['file'])
                db_feature = FeatureEntries.objects.create(date=datetime.strptime(data_date, '%d_%m_%y'))
                func.InsertFeature2DB(fe.genfeatureFromCSV(raw.file.path, 600), db_feature)
                if FileTracker.objects.count() == 0:
                    FileTracker.objects.create(accCount=1)
                else:
                    #print(FileTracker.objects.count())
                    obj = FileTracker.objects.first()
                    obj.accCount += 1
                    obj.save()
                    uploaded = True
                    print("A file has been uploaded to /media/data.")
                    if obj.accCount == 20:
                        #TODO: add machine learning stuff here
                        pass
            else:
                print("A duplicate has been detected, not uploaded.")
        else:
            print(f_form.errors)
            print(f_form.non_field_errors)
    return render(request, "ml/ml_homepage.html", {'uploaded': uploaded,
                                                    'count': RawData.objects.count(),
                                                    })

#remember to set X-CSRFTOKEN in headers, then JSON in body under application/json
def add_raw_data(request):
    '''
    need to check username, then see if username.date file exists
    if not, create, with headers
    if so, append (check latest datetime maybe?)
    '''
    if request.method == "POST":
        json_data = json.loads(request.body.decode("utf-8"))

        username = json_data['username']

        date = datetime.now().strftime("%d_%m_%y")

        path = os.path.join(settings.MEDIA_ROOT, 'data')
        path = os.path.join(path, username)
        path = os.path.join(path, file_prefix + date + ".csv")
        exist = check_duplicate(file_prefix+date+".csv", username)

        if not exist:
            try:
                csv_insert_header(path, ["Time", "HR", "RR", "Mode", "GSR", "SkinT", "AccX", "AccY", "AccZ", "outcome"])
            except IOError:
                messages.error(request, 'error while inserting header')
        else:
            last_row = get_last_row(path)[0]

            #get timestamp of last row, then format it into datetime
            #if no data, so only header, then create a datetime of epoch
            if last_row != "Time":
                last_time = datetime.strptime(last_row, '%d/%m/%y %H:%M:%S').strftime("%d/%m/%y %H:%M:%S")
            else:
                last_time = datetime.utcfromtimestamp(0).strftime("%d/%m/%y %H:%M:%S")

            for data in json_data['data']:
                try:
                    timestamp = datetime.strptime(data["timestamp"], "%d/%m/%y %H:%M:%S").strftime("%d/%m/%y %H:%M:%S")

                    #only append if timestamp of data is newer than last line
                    #last_time only refreshes once, so this won't deal with new, but out of order data
                    #lasttime is 21:00:00, then new data is 21:53:53, then 21:53:54 OK
                    #lasttime is 22:00:00, then new data is 21:53:53, then 21:53:54 SKIPPED
                    #lasttime is 21:00:00, then new data is 21:53:53, then 21:53:00 OK (as last time checks once)
                    if last_time < timestamp:
                        csv_append(path, [
                            timestamp,
                            data["HR"],
                            data["RR"],
                            data["mode"],
                            data["GSR"],
                            data["SkinT"],
                            data["AccX"],
                            data["AccY"],
                            data["AccZ"],
                            data["outcome"],
                        ])
                    else:
                        print("skipping due to previous entry")

                except IOError:
                    messages.error(request, 'error while appending csv')
        messages.success(request, 'success')
    else:
        messages.warning(request, 'not a post request')
    return render(request, "ml/post.html", {'json_data': json_data})


def csv_append(filename, data):
    with open(filename, 'a', newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(data)
        return True
    return IOError

def csv_insert_header(filename, header):
    open(filename, 'a', newline='').close()
    with open(filename, 'w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(header)
        return True
    return IOError

def get_last_row(filename):
    with open(filename, 'r', newline='') as f:
        try:
            lastrow = deque(csv.reader(f), 1)[0]
        except IndexError:  # empty file
            lastrow = None
        return lastrow

def home(request):
    return render(request, "ml/ml_homepage.html", {'uploaded': False,
                                                'fileForm': FileForm()})
