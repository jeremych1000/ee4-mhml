from django.conf import settings
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

import json, requests

class PushyAPI:
        @staticmethod
        def sendPushNotification(data, tokens, notification):
                # Insert your Pushy Secret API Key here
                apiKey = settings.PUSHY_API_KEY;
                url = 'https://api.pushy.me/push?api_key=' + apiKey

                # Set post variables
                payload = {
                    "to": tokens,
                    "data": {
                        "message": "iiiiii"
                    },
                    "notification": notification,
                }
                headers = {
                    'Content-Type': 'application/json',
                }
                # Set URL to Send Notifications API endpoint
                r = requests.post(url, data=json.dumps(payload), headers=headers)
                return r

class push(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        data = {
            'message': 'WWWWWWWWWWWWWWWWWW'
        }
        notification = {
            "body": "WWWWWWWWWWWWWWWWW \u1F984",
            "badge": 1,
            "sound": "ping.aiff"
        }

        # The recipient device tokens
        deviceTokens = 'd568b298815928ac4723c1'

        # Send the push notification with Pushy
        ret = PushyAPI.sendPushNotification(data, deviceTokens, notification)

        return Response(ret.json(), status=status.HTTP_200_OK)