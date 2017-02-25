from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os
import csv
import numpy as np
import math


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


datapath=os.path.join('..',os.path.join('media','data'))
features =[]
outcomes=[]
dates=[]

for file in os.listdir(datapath):
    if file.endswith(".csv"):
        filepath = os.path.join(datapath, file)
        new_d, new_f, new_out = CSV2Feature(filepath, 600)
        features += (new_f)
        outcomes += new_out
        dates += new_d

train_f,test_f,train_o,test_o=train_test_split(features, outcomes, test_size=0.2,random_state=0)
clf = RandomForestClassifier()
clf.fit(train_f,train_o)
test_r= clf.predict(test_f)
print(test_r)
print(test_o)
count=0
acc=sum([r==o for r,o in zip(test_r,test_o)])/len(test_r)
print(acc)
print(clf.feature_importances_)