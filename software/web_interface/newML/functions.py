import numpy as np
import math
from sklearn.ensemble import RandomForestClassifier
from newML import models
import pickle
import os
import csv
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
from datetime import timedelta

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
        user_object = User.objects.get(username=username)

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


def FeatureEntry2FeatureOutcome(entryVec):
    features = [];
    outcomes = [];
    for f in entryVec:
        features.append(
            [f.mean_hr, f.std_hr, f.mean_rr, f.std_rr, f.mean_gsr, f.std_gsr, f.mean_temp, f.std_temp, f.mean_acc])
        outcomes.append(f.label)
    return features, outcomes


def createNewModel(username):
    # get username from user database
    user_object = User.objects.get(username=username)
    feature_vec = models.FeatureEntry.objects.all().filter(user=user_object, label__isnull=False)
    if len(feature_vec) != 0:
        model_path = os.path.join(settings.MEDIA_ROOT, os.path.join('model', username + '.p'))
        p_list = os.listdir(os.path.join(settings.MEDIA_ROOT, 'model'))
        file_mode = 'wb'
        # for x in p_list:
        #     if username + '.p' == x:
        #         file_mode = 'rb'
        filehandle = open(model_path, file_mode)
        features, outcomes = FeatureEntry2FeatureOutcome(feature_vec)
        clf = RandomForestClassifier()
        clf.fit(features, outcomes)
        models.ModelFile.objects.create(file=model_path, user=user_object)
        pickle._dump(clf, filehandle)
        return clf
    else:
        # load default model

        # get username from user database
        user_object = User.objects.get(username="Default")

        default_obj = models.ModelFile.objects.all().filter(user=user_object).first()
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


def labelInsertion(json):
    start_date = datetime.strptime(json["start"], '%d/%m/%y %H:%M:%S').date()
    end_date = datetime.strptime(json["stop"], '%d/%m/%y %H:%M:%S').date()
    end_date+=timedelta(days=1)
    print('starting date: ',end_date)
    print('stoping date: ',end_date)
    outcome = True if json["quality"] == 1 else False
    username = json["username"]
    user = models.User.objects.get(username=username)
    unlabelFeature = models.FeatureEntry.objects.all().filter(user=user, date__range=(start_date, end_date),
                                                              label__isnull=True)
    for fObj in unlabelFeature:
        fObj.label = outcome
        fObj.save()
    print('Inserted ',len(unlabelFeature),' label')
    modelObj=models.ModelFile.objects.get(user=user)
    print('Untrained Feature for  ', username,': ' ,modelObj.untrained)
    if modelObj:
        modelObj.untrained+=len(unlabelFeature)
        modelObj.save()
        if modelObj.untrained>5:
            print('Retraining model...')
            print('Loading from ',modelObj.file.path)
            modelfile=open(modelObj.file.path,'rb')
            clf = pickle.load(modelfile)
            modelfile.close()
            featureEntryVec = models.FeatureEntry.objects.all().filter(user=user,label__isnull=False)
            feature,outcome=FeatureEntry2FeatureOutcome(featureEntryVec)
            clf.fit(feature,outcome)
            modelfile = open(modelObj.file.path, 'wb')
            pickle._dump(clf,modelfile)
            modelfile.close()
            modelObj.untrained=0
            modelObj.save()
            print('Retraining model...Done!')
