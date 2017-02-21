import numpy as np
import math
from sklearn.ensemble import RandomForestClassifier
from newML import models
import pickle
import os
import csv
from django.conf import settings
from django.contrib.auth.models import User


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
            hr.append(float(data["HR"]))
            rr.append(float(data["RR"]))
            gsr.append(float(data["GSR"]))
            temp.append(float(data["SkinT"]))
            accX.append(float(data["AccX"]))
            accY.append(float(data["AccY"]))
            accZ.append(float(data["AccZ"]))
        feature["mean_hr"] = np.mean(hr)
        feature["std_hr"] = np.std(hr)
        feature["mean_rr"] = np.mean(rr)
        feature["std_rr"] = np.std(rr)
        feature["mean_gsr"] = np.mean(gsr)
        feature["std_gsr"] = np.std(gsr)
        feature["mean_temp"] = np.mean(temp)
        feature["std_temp"] = np.std(temp)
        feature["mean_acc"] = np.mean([math.sqrt(x ** 2 + y ** 2 + z ** 2) for x, y, z in zip(accX, accY, accZ)])

        # get username from user database
        user_object = User.objects.all().filter(username=username).first()

        models.FeatureEntry.objects.create(date=timestamp,
                                           user=user_object,
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
    # get username from user database
    user_object = User.objects.all().filter(username=username).first()
    feature_vec = models.FeatureEntry.objects.all().filter(user=user_object, label__isnull=False)
    if len(feature_vec) != 0:
        model_path = os.path.join(settings.MEDIA_ROOT, 'model/' + username + '.p')
        filehandle = open(model_path, 'rb')
        clf = RandomForestClassifier.fit(feature_vec)
        models.ModelFile.objects.create(file=filehandle, username=username)
        pickle._dump(clf, filehandle)
        return clf
    else:
        # load default model

        # get username from user database
        user_object_default = User.objects.all().filter(username="Default").first()

        default_obj = models.ModelFile.objects.all().filter(user=user_object_default).first()
        def_clf = pickle._load(default_obj.file)
        return def_clf


def storeModel(path, clf):
    pickle.dumps(clf, open(path, 'wb'))


def CSV2Feature(fileURL, winSize):
    fHandle = open(fileURL)
    csvReader = csv.reader(fHandle)
    csvReader.__next__()
    rowCount = winSize
    winSlice = []
    features = []
    outcomes = []
    outcome = False
    dateVecs = []
    for row in csvReader:
        if len(row) == 10:
            outcome = (row[9] == "true" or row[9] == "True" or row[9] == "TRUE")
        if rowCount != 0:
            winSlice.append(row)
            rowCount -= 1
        else:
            winSlice = np.array(winSlice)
            hr_slice = [float(ele[1]) for ele in winSlice]
            rr_slice = [float(ele[2]) for ele in winSlice]
            gsr_slice = [float(ele[4]) for ele in winSlice]
            temp_slice = [float(ele[5]) for ele in winSlice]
            acc_slice = [math.sqrt(float(ele[6]) ** 2 + float(ele[7]) ** 2 + float(ele[8]) ** 2) for ele in winSlice]
            features.append(
                [np.mean(hr_slice), np.std(hr_slice), np.mean(rr_slice), np.std(rr_slice), np.mean(gsr_slice),
                 np.std(gsr_slice), np.mean(temp_slice), np.std(temp_slice), np.mean(acc_slice)])
            outcomes.append(outcome)
            dateVecs.append(winSlice[0][0])
            rowCount = winSize
            winSlice = []

    if len(winSlice) != 0:
        winSlice = np.array(winSlice)
        hr_slice = [float(ele[1]) for ele in winSlice]
        rr_slice = [float(ele[2]) for ele in winSlice]
        gsr_slice = [float(ele[4]) for ele in winSlice]
        temp_slice = [float(ele[5]) for ele in winSlice]
        acc_slice = [math.sqrt(float(ele[6]) ** 2 + float(ele[7]) ** 2 + float(ele[8]) ** 2) for ele in winSlice]
        dateVecs.append(winSlice[0][0])
        features.append([np.mean(hr_slice), np.std(hr_slice), np.mean(rr_slice), np.std(rr_slice), np.mean(gsr_slice),
                         np.std(gsr_slice), np.mean(temp_slice), np.std(temp_slice), np.mean(acc_slice)])
        outcomes.append(outcome)

    return dateVecs, features, outcomes
