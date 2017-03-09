import os
from django.conf import settings
from django.http import HttpResponseRedirect
import newML.functions as func
from sklearn.ensemble import RandomForestClassifier
import pickle
from newML import models
from django.contrib.auth.models import User
from datetime import datetime

def settingDefault(request):
    model_path = os.path.join(settings.MEDIA_ROOT, os.path.join('model', 'default.p'))
    data_path = os.path.join(settings.MEDIA_ROOT, 'data')

    f_handle = open(model_path, 'wb')
    features = []
    outcomes = []
    for file in os.listdir(data_path):
        if file.endswith(".csv"):
            filepath = os.path.join(data_path, file)
            new_d, new_f, new_out = func.CSV2Feature(filepath, 600)
            features += (new_f)
            outcomes += new_out
    clf = RandomForestClassifier(n_estimators = 30)
    clf.fit(features, outcomes)
    pickle.dump(clf, f_handle)
    return HttpResponseRedirect('/')


def migrateFeature(request):
    username = "jeremych"
    userObj = User.objects.get(username=username)
    data_path = os.path.join(settings.MEDIA_ROOT, os.path.join('data',username))
    features = []
    outcomes = []
    dates = []
    for file in os.listdir(data_path):
        if file.endswith(".csv"):
            filepath = os.path.join(data_path, file)
            new_d, new_f, new_out = func.CSV2Feature(filepath, 600)
            features += (new_f)
            outcomes += new_out
            dates += new_d
            models.NightRecord.objects.create(user=userObj,start_date=datetime.strptime(new_d[0],'%d/%m/%y %H:%M:%S'),end_date=datetime.strptime(new_d[-1],'%d/%m/%y %H:%M:%S'))

    for d, f, o in zip(dates, features, outcomes):
        d_obj = datetime.strptime(d,'%d/%m/%y %H:%M:%S')
        models.FeatureEntry.objects.create(user=userObj, date=d_obj, mean_hr=f[0], std_hr=f[1], mean_rr=f[2], std_rr=f[3],
                                           mean_gsr=f[4], std_gsr=f[5], mean_temp=f[6], std_temp=f[7], mean_acc=f[8],kurt_hr=f[9],
                                           kurt_rr=f[10],
                                           kurt_gsr=f[11],
                                           label=o)
    return HttpResponseRedirect('/')
