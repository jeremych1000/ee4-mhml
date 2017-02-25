from rest_framework import serializers
from newML.models import FeatureEntry

class FeatureEntrySerializer(serializers.ModelSerializer):
    class Meta:
        # query returns FeatureEntry objects
        model = FeatureEntry
        fields = ('date', 'mean_temp', 'std_temp')