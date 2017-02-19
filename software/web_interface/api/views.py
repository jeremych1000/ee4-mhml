from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import random

def random_number(bits):
    return random.getrandbits(bits)

def random_outcome(request):
    a = random.getrandbits(1)
    return HttpResponse(a)

class random_api(APIView):
    def get(self, request):
        result = random_number(1)
        response = Response(result, status=status.HTTP_200_OK)
        return response

    def post(self, request):
        


