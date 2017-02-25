from rest_framework import serializers
from newML.models import FeatureEntry

class FeatureEntrySerializer():
    class heartrate(serializers.ModelSerializer):
        class Meta:
            # query returns FeatureEntry objects
            model = FeatureEntry
            fields = ('date', 'mean_hr')

    class rr(serializers.ModelSerializer):
        class Meta:
            # query returns FeatureEntry objects
            model = FeatureEntry
            fields = ('date', 'mean_rr')

    class gsr(serializers.ModelSerializer):
        class Meta:
            # query returns FeatureEntry objects
            model = FeatureEntry
            fields = ('date', 'mean_gsr')


    class temperature(serializers.ModelSerializer):
        class Meta:
            # query returns FeatureEntry objects
            model = FeatureEntry
            fields = ('date', 'mean_temp')

    class acceleration(serializers.ModelSerializer):
        class Meta:
            # query returns FeatureEntry objects
            model = FeatureEntry
            fields = ('date', 'mean_acc')