from django.contrib import admin
from MLBlock.models import *

# Register your models here.
admin.site.register(RawData)
admin.site.register(FileTracker)
admin.site.register(FeatureEntries)
admin.site.register(MeanHR)
admin.site.register(StdHR)
admin.site.register(MeanRR)
admin.site.register(StdRR)
admin.site.register(MeanGSR)
admin.site.register(StdGSR)
admin.site.register(MeanTemp)
admin.site.register(StdTemp)
admin.site.register(MeanAcc)
admin.site.register(SleepQuality)