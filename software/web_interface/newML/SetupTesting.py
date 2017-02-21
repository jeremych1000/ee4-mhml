import os
from django.conf import settings
from django.http import HttpResponseRedirect
import newML.functions as func
from sklearn.ensemble import RandomForestClassifier
import pickle
from newML import models
from django.core.files import File


def settingDefault(request):
    model_path = os.path.join(settings.MEDIA_ROOT, os.path.join('model', 'default.p'))
    data_path = os.path.join(settings.MEDIA_ROOT, 'data')

    f_handle = open(model_path, 'wb')
    features = []
    outcomes = []
    for file in os.listdir(data_path):
        if file.endswith(".csv"):
            filepath = os.path.join(data_path, file)
            new_f, new_out = func.genfeatureFromCSV(filepath, 600)
            features += (new_f)
            outcomes += new_out
    clf = RandomForestClassifier()
    clf.fit(features, outcomes)
    pickle.dump(clf, f_handle)
    models.ModelFile.objects.create(file=model_path, username='Default')
    return HttpResponseRedirect('/')

def migrateFeature(request):
    data_path = os.path.join(settings.MEDIA_ROOT, 'data')
    features = []
    outcomes = []
    for file in os.listdir(data_path):
        if file.endswith(".csv"):
            filepath = os.path.join(data_path, file)
            new_f, new_out = func.genfeatureFromCSV(filepath, 600)
            features += (new_f)
            outcomes += new_out
    for f,o in zip(features,outcomes):
        models.FeatureEntry.objects.create()

    return HttpResponseRedirect('/')
