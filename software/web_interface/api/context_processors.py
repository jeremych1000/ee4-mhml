from django.contrib.auth.models import User
from newML.models import FeatureEntry

def quick_stats(request):
    user_object = User.objects.get(username=request.user)

    user_feature_entries = FeatureEntry.objects.all().filter(user=user_object)

    total_entries = len(user_feature_entries)


    return {
        "current_user": user_object,
        "total_entries": total_entries,
    }
