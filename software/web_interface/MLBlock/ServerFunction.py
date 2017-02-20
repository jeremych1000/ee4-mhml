from MLBlock.models import *

def InsertFeature2DB(featureVec,DBFeature, Username=None):
    for index in range(0,len(featureVec[0])):
        MeanHR.objects.create(data=featureVec[0][index],featureEntry=DBFeature, username=Username)
        StdHR.objects.create(data=featureVec[1][index], featureEntry=DBFeature, username=Username)
        MeanRR.objects.create(data=featureVec[2][index], featureEntry=DBFeature, username=Username)
        StdRR.objects.create(data=featureVec[3][index], featureEntry=DBFeature, username=Username)
        MeanGSR.objects.create(data=featureVec[4][index], featureEntry=DBFeature, username=Username)
        StdGSR.objects.create(data=featureVec[5][index], featureEntry=DBFeature, username=Username)
        MeanTemp.objects.create(data=featureVec[6][index], featureEntry=DBFeature, username=Username)
        StdTemp.objects.create(data=featureVec[7][index], featureEntry=DBFeature, username=Username)
        MeanAcc.objects.create(data=featureVec[8][index], featureEntry=DBFeature, username=Username)
    SleepQuality.objects.create(data=featureVec[9],featureEntry=DBFeature, username=Username)
