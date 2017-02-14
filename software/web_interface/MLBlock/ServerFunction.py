from MLBlock.models import *

def InsertFeature2DB(featureVec,DBFeature):
    for index in range(0,len(featureVec[0])):
        MeanHR.objects.create(data=featureVec[0][index],featureEntry=DBFeature)
        StdHR.objects.create(data=featureVec[1][index], featureEntry=DBFeature)
        MeanRR.objects.create(data=featureVec[2][index], featureEntry=DBFeature)
        StdRR.objects.create(data=featureVec[3][index], featureEntry=DBFeature)
        MeanGSR.objects.create(data=featureVec[4][index], featureEntry=DBFeature)
        StdGSR.objects.create(data=featureVec[5][index], featureEntry=DBFeature)
        MeanTemp.objects.create(data=featureVec[6][index], featureEntry=DBFeature)
        StdTemp.objects.create(data=featureVec[7][index], featureEntry=DBFeature)
        MeanAcc.objects.create(data=featureVec[8][index], featureEntry=DBFeature)
    SleepQuality.objects.create(data=featureVec[9],featureEntry=DBFeature)
