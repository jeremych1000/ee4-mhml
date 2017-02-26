from rest_framework import serializers
from newML.models import FeatureEntry


class FeatureEntrySerializer():
    class mean_hr(serializers.ModelSerializer):
        class Meta:
            # query returns FeatureEntry objects
            model = FeatureEntry
            fields = ('date', 'mean_hr',)

    class std_hr(serializers.ModelSerializer):
        class Meta:
            # query returns FeatureEntry objects
            model = FeatureEntry
            fields = ('date', 'std_hr',)

    class mean_rr(serializers.ModelSerializer):
        class Meta:
            # query returns FeatureEntry objects
            model = FeatureEntry
            fields = ('date', 'mean_rr')

    class std_rr(serializers.ModelSerializer):
        class Meta:
            # query returns FeatureEntry objects
            model = FeatureEntry
            fields = ('date', 'std_rr')

    class mean_gsr(serializers.ModelSerializer):
        class Meta:
            # query returns FeatureEntry objects
            model = FeatureEntry
            fields = ('date', 'mean_gsr')

    class std_gsr(serializers.ModelSerializer):
        class Meta:
            # query returns FeatureEntry objects
            model = FeatureEntry
            fields = ('date', 'std_gsr')

    class mean_temp(serializers.ModelSerializer):
        class Meta:
            # query returns FeatureEntry objects
            model = FeatureEntry
            fields = ('date', 'mean_temp')

    class std_temp(serializers.ModelSerializer):
        class Meta:
            # query returns FeatureEntry objects
            model = FeatureEntry
            fields = ('date', 'std_temp')

    class mean_acc(serializers.ModelSerializer):
        class Meta:
            # query returns FeatureEntry objects
            model = FeatureEntry
            fields = ('date', 'mean_acc')

    class std_acc(serializers.ModelSerializer):
        class Meta:
            # query returns FeatureEntry objects
            model = FeatureEntry
            fields = ('date', 'std_acc')
