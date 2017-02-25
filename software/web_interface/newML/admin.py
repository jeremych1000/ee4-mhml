from django.contrib import admin
from newML import models
# Register your models here.
admin.site.register(models.FeatureEntry)
admin.site.register(models.ModelFile)
admin.site.register(models.TempProfile)
admin.site.register(models.NightRecord)