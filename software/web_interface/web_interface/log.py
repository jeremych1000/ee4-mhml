from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views import View
import os


class log(View):
    def get(self, request):
        if request.user.is_authenticated():
            path = os.path.join(settings.STATICFILES_DIRS[0], 'log.log')
            # print(path)
            with open(path, 'rb') as myfile:
                data = myfile.read()
            return HttpResponse(data, content_type='text/plain')
        else:
            return HttpResponse("Please login to view.", content_type='text/plain', status=401)