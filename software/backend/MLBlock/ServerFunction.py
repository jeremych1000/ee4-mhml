from MLBlock.models import *

def InsertFeature2DB(featureVec,DBFeature):
    for index in range(0,len(featureVec[0])):
        MeanHR.objects.create(data=featureVec[0][index],featureEntry=DBFeature)
        StdHR.objects.create(data=featureVec[0][index], featureEntry=DBFeature)
        MeanRR.objects.create(data=featureVec[0][index], featureEntry=DBFeature)
        StdRR.objects.create(data=featureVec[0][index], featureEntry=DBFeature)
        MeanGSR.objects.create(data=featureVec[0][index], featureEntry=DBFeature)
        StdGSR.objects.create(data=featureVec[0][index], featureEntry=DBFeature)
        MeanTemp.objects.create(data=featureVec[0][index], featureEntry=DBFeature)
        StdTemp.objects.create(data=featureVec[0][index], featureEntry=DBFeature)
        MeanAcc.objects.create(data=featureVec[0][index], featureEntry=DBFeature)
