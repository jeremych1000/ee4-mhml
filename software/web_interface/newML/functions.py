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
from scipy import stats as st


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
        feature["kurt_hr"] = st.kurtosis(hr)
        feature["kurt_rr"] = st.kurtosis(rr)
        feature["kurt_gsr"] = st.kurtosis(gsr)
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
                                           kurt_hr=feature['kurt_hr'],
                                           kurt_rr=feature['kurt_rr'],
                                           kurt_gsr=feature['kurt_gsr'],
                                           label=None
                                           )

        return [feature["mean_hr"], feature["std_hr"], feature["mean_rr"], feature["std_rr"], feature["mean_gsr"],
                feature["std_gsr"], feature["mean_temp"], feature["std_temp"], feature["mean_acc"],feature["kurt_hr"],feature["kurt_gsr"],feature["kurt_rr"]]


def FeatureEntry2FeatureOutcome(entryVec):
    features = [];
    outcomes = [];
    for f in entryVec:
        features.append(
            [f.mean_hr, f.std_hr, f.mean_rr, f.std_rr, f.mean_gsr, f.std_gsr, f.mean_temp, f.std_temp, f.mean_acc,f.kurt_hr,f.kurt_rr,f.kurt_gsr])
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
                 np.std(gsr_slice), np.mean(temp_slice), np.std(temp_slice), np.mean(acc_slice),st.kurtosis(hr_slice),st.kurtosis(rr_slice),st.kurtosis(gsr_slice)])
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
                         np.std(gsr_slice), np.mean(temp_slice), np.std(temp_slice), np.mean(acc_slice),st.kurtosis(hr_slice),st.kurtosis(rr_slice),st.kurtosis(gsr_slice)])
        outcomes.append(outcome)

    return dateVecs, features, outcomes


def labelInsertion(json):
    start_date = datetime.strptime(json["start"], '%d/%m/%y %H:%M:%S').date()
    end_date = datetime.strptime(json["stop"], '%d/%m/%y %H:%M:%S').date()
    end_date += timedelta(days=1)

    print('starting date: ', start_date)
    print('stoping date: ', end_date)
    outcome = True if json["quality"] == 1 else False
    username = json["username"]
    user = models.User.objects.get(username=username)
    models.NightRecord.objects.create(user=user, start_date=start_date, end_date=end_date)
    unlabelFeature = models.FeatureEntry.objects.all().filter(user=user, date__range=(start_date, end_date),
                                                              label__isnull=True)
    for fObj in unlabelFeature:
        fObj.label = outcome
        fObj.save()

    print("Update Heat Profile....")
    print(UpdateTempProfile(username))
    print('Inserted ', len(unlabelFeature), ' label')
    modelObj = models.ModelFile.objects.get(user=user)
    print('Untrained Feature for  ', username, ': ', modelObj.untrained)
    if modelObj:
        modelObj.untrained += len(unlabelFeature)
        modelObj.save()
        if modelObj.untrained > 5:
            print('Retraining model...')
            print('Loading from ', modelObj.file.path)
            modelfile = open(modelObj.file.path, 'rb')
            clf = pickle.load(modelfile)
            modelfile.close()
            featureEntryVec = models.FeatureEntry.objects.all().filter(user=user, label__isnull=False)
            feature, outcome = FeatureEntry2FeatureOutcome(featureEntryVec)
            clf.fit(feature, outcome)
            modelfile = open(modelObj.file.path, 'wb')
            pickle._dump(clf, modelfile)
            modelfile.close()
            modelObj.untrained = 0
            modelObj.save()
            print('Retraining model...Done!')


def UpdateTempProfile(username):
    userObj = User.objects.get(username=username)
    if userObj == None:
        return 'User not Found'
    records = models.NightRecord.objects.all().filter(user=userObj)
    if len(records) == 0:
        return 'User record not Found'
    # get all features
    allFeatures = models.FeatureEntry.objects.all().filter(user=userObj).extra(order_by=['id'])
    if len(allFeatures) == 0:
        return 'User Features not Found'
    # Filter each night and build matrix of each night temp with good sleep quality
    goodNightTemps = []
    for record in records:
        featureInEachNight = list(filter(lambda x: (x.date <= record.end_date) and (x.date >= record.start_date),
                                    allFeatures))
        if featureInEachNight[0].label == True:
            goodNightTemps .append([x.mean_temp for x in featureInEachNight])
    # segmentized into 4 equal region for each night
    if len(goodNightTemps) == 0:
        return 'Good night data not Found'
    meanInEachNight = []
    for tempVec in goodNightTemps:

        mod4 = divmod(len(tempVec), 4)
        segmentSize = math.ceil(len(tempVec) / 4)
        segmentMean = [0,0,0,0]
        if mod4 == 0:
            for i in range(0, 4):
                segmentMean[i] = np.mean(tempVec[i * segmentSize:(i + 1) * segmentSize - 1])
        else:
            for i in range(0, 3):
                segmentMean[i] = np.mean(tempVec[i * segmentSize:(i + 1) * segmentSize - 1])
            print(len(tempVec))
            print(3 * segmentSize - 1)
            segmentMean[3] = np.mean(tempVec[3 * segmentSize - 1:])
        meanInEachNight .append( segmentMean)
    # cross nights mean aggreate
    optimalMean = np.mean(meanInEachNight, axis=0)
    # update heat profile
    profileObj = models.TempProfile.objects.all().filter(user=userObj)
    if len(profileObj) == 0:
        for j in range(0, 4):
            models.TempProfile.objects.create(user=userObj, period=j, value=optimalMean[j])
    else:
        for j in range(0, 4):
            profileObj = profileObj.filter(period=j)
            profileObj.value = profileObj.value + optimalMean[j] / 2  # Average with new mean temp
            profileObj.save()
    return "Update profile Success"


def getTempProfile(username):
    userObj = User.objects.get(username=username)
    allTemp = models.TempProfile.objects.all().filter(user=userObj)
    result = [34,34,34,34]
    for i in range(0, 3):
        ob = allTemp.filter(period=i).first()
        result[i] = ob.value
    return result

def getFeatureInRange(username,start_date,end_date):
    userObj = User.objects.get(username=username)
    if userObj == None:
        return 'User not Found'
    # get all features
    allFeatures = models.FeatureEntry.objects.all().filter(user=userObj).extra(order_by=['id'])
    if len(allFeatures) == 0:
        return 'User Features not Found'
    # Filter each night and build matrix of each night temp with good sleep quality
    featureInEachNight = list(filter(lambda x: (x.date.date() <= end_date.date()) and (x.date.date() >= start_date.date()),
                                allFeatures))
    #print(featureInEachNight, type(featureInEachNight))
    return featureInEachNight
