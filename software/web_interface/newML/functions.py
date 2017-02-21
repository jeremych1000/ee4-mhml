import numpy as np
import math
from sklearn.ensemble import RandomForestClassifier
from newML import models
import pickle
import os
from django.conf import settings


def json2Feature(json, username, timestamp):
    if 'data' not in json.keys():
        assert 'JSON is missing the data array'
    else:
        hr = [];
        rr = [];
        gsr = [];
        temp = [];
        accX = [];
        accY = [];
        accZ = [];
        feature = {};
        for data in json.get('data'):
            hr.append(data["HR"])
            rr.append(data["RR"])
            gsr.append(data["GSR"])
            temp.append(data["SkinT"])
            accX.append(data["AccX"])
            accY.append(data["AccY"])
            accZ.append(data["AccZ"])
        feature["mean_hr"] = np.mean(hr)
        feature["std_hr"] = np.std(hr)
        feature["mean_rr"] = np.mean(rr)
        feature["std_rr"] = np.std(rr)
        feature["mean_gsr"] = np.mean(gsr)
        feature["std_gsr"] = np.std(gsr)
        feature["mean_temp"] = np.mean(temp)
        feature["std_temp"] = np.std(temp)
        feature["mean_acc"] = np.mean([math.sqrt(x ** 2 + y ** 2 + z ** 2) for x, y, z in zip(accX, accY, accZ)])
        models.FeatureEntry.objects.create(date=timestamp,
                                           username=username,
                                           mean_hr=feature['mean_hr'],
                                           std_hr=feature['std_hr'],
                                           mean_rr=feature['mean_rr'],
                                           std_rr=feature['std_rr'],
                                           mean_gsr=feature['mean_gsr'],
                                           std_gsr=feature['std_gsr'],
                                           mean_temp=feature['mean_temp'],
                                           std_temp=feature['std_temp'],
                                           mean_acc=feature['mean_acc'],
                                           label=None
                                           )

        return [feature["mean_hr"], feature["std_hr"], feature["mean_rr"], feature["std_rr"], feature["mean_gsr"],
                feature["std_gsr"], feature["mean_temp"], feature["std_temp"], feature["mean_acc"]]


def getMLObj(path):
    pass


def createNewModel(username):
    feature_vec = models.FeatureEntry.objects.all().filter(username=username, label__isnull=False)
    if len(feature_vec) != 0:
        model_path = os.path.join(settings.MEDIA_ROOT, 'model/' + username+'.p')
        filehandle = open(model_path, 'rb')
        clf = RandomForestClassifier.fit(feature_vec)
        models.ModelFile.objects.create(file=filehandle, username=username)
        pickle._dump(clf, filehandle)
        return clf
    else:
        # load default model
        default_obj = models.ModelFile.objects.all().filter(username="default")
        path = default_obj.file.path
        def_clf = pickle._load(open(path, 'rb'));
        return def_clf


def storeModel(path, clf):
    pickle.dumps(clf, open(path, 'wb'))
    

