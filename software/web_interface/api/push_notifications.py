from django.conf import settings
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from myaccount import models

import json, requests

class PushyAPI:
        @staticmethod
        def sendPushNotification(data, tokens, notification):
                # Insert your Pushy Secret API Key here
                apiKey = settings.PUSHY_API_KEY
                url = 'https://api.pushy.me/push?api_key=' + apiKey

                # Set post variables
                payload = {
                    "to": tokens,
                    "data": data,
                    "notification": notification,
                }
                headers = {
                    'Content-Type': 'application/json',
                }
                # Set URL to Send Notifications API endpoint
                r = requests.post(url, data=json.dumps(payload), headers=headers)
                return r.json()

class push(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        data = {
            'message': 'WWWWWWWWWWWWWWWWWW'
        }
        notification = {
            "body": "time to go to school! \u1F984",
            "badge": 1,
            "sound": "ping.aiff"
        }

        # The recipient device tokens
        token_obj = models.PushyToken.objects.all()

        json_ret = []
        for i in token_obj:
            ret = PushyAPI.sendPushNotification(data, i.token, notification)
            json_ret.append(ret)
        return Response(json_ret, status=status.HTTP_200_OK)