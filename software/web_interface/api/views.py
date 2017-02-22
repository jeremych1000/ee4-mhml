from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

import newML.functions
from newML import models as ml_model
from datetime import datetime

import os, re, json, random
from . import csv_functions

import numpy as np
import pickle
from MLBlock.views import insert_from_api


class random_number(APIView):
    def get(self, request):
        result = random.getrandbits(1)
        return Response(result, status=status.HTTP_200_OK)


class raw_data(APIView):
    file_prefix = "MSBand2_ALL_data_"

    def post(self, request):
        json_data = json.loads(request.body.decode("utf-8"))
        print("DEBUG: ", json_data)

        username = json_data['username']

        date = datetime.now().strftime("%d_%m_%y")

        path = os.path.join(settings.MEDIA_ROOT, 'data')
        path = os.path.join(path, username)

        filename = raw_data.file_prefix + date + ".csv"
        final_path = os.path.join(path, filename)

        exist = csv_functions.check_duplicate(raw_data.file_prefix + date + ".csv", username)

        if not exist:
            try:
                # print (path, "---", final_path)
                csv_functions.csv_insert_header(path, final_path,
                                                ["Time", "HR", "RR", "Mode", "GSR", "SkinT", "AccX", "AccY", "AccZ",
                                                 "outcome"])
            except IOError:
                messages.error(request, 'error while inserting header')

            last_time = datetime.utcfromtimestamp(0).strftime("%d/%m/%y %H:%M:%S")
        else:
            last_row = csv_functions.get_last_row(final_path)[0]
            last_time = datetime.strptime(last_row, '%d/%m/%y %H:%M:%S').strftime("%d/%m/%y %H:%M:%S")

        # begin data extraction from JSOn

        HR = []

        for data in json_data['data']:
            timestamp = datetime.strptime(data["timestamp"], "%d/%m/%y %H:%M:%S").strftime("%d/%m/%y %H:%M:%S")

            # only append if timestamp of data is newer than last line
            # last_time only refreshes once, so this won't deal with new, but out of order data
            # lasttime is 21:00:00, then new data is 21:53:53, then 21:53:54 OK
            # lasttime is 21:00:00, then new data is 20:53:53, then 20:53:54 SKIPPED
            # lasttime is 21:00:00, then new data is 21:53:53, then 21:53:50 OK (as last time checks once)
            success = False

            if last_time < timestamp:
                try:
                    success = csv_functions.csv_append(final_path, [
                        timestamp,
                        data["HR"],
                        data["RR"],
                        data["mode"],
                        data["GSR"],
                        data["SkinT"],
                        data["AccX"],
                        data["AccY"],
                        data["AccZ"],
                        data["outcome"],
                    ])

                    json_result = {"success": success, "reason": "Raw data successfully appended to data file."}
                except IOError:
                    messages.error(request, 'error while appending csv')
                    json_result = {"success": success, "reason": "Error while appending to data file."}
            else:
                json_result = {"success": success, "reason": "Skipping due to old entry."}

        return Response(json_result, status=status.HTTP_200_OK)


class on_off(APIView):
    def get(self, request):
        json = random.getrandbits(1)
        return Response(json, status=status.HTTP_200_OK)

class realTimeResponse(APIView):
    def post(self, request):
        json_result = {}
        json_data = json.loads(request.body.decode("utf-8"))
        print("DEBUG: ", json_data)
        username = json_data['username']
        data = json_data["data"]
        timestamp = datetime.strptime(data[-1]["timestamp"], "%d/%m/%y %H:%M:%S")
        feature = newML.functions.json2Feature(json_data, username, timestamp)
        user_object = User.objects.get(username=username)
        mlfile = ml_model.ModelFile.objects.all().filter(user=user_object).first()
        if not mlfile:
            classifier = newML.functions.createNewModel(username)
        else:
            classifier = pickle.load(open(mlfile.file.path, 'rb'))
        feature = np.array([feature])
        outcome = classifier.predict(feature)
        json_result["quality"] = outcome[0]
        return Response(json_result, status=status.HTTP_200_OK)

class userFeedback(APIView):
    def post(self,request):
        json_data = json.loads(request.body.decode("utf-8"))
        newML.functions.labelInsertion(json_data)
        return Response( status=status.HTTP_200_OK)

class stats():
    class temperature():
        class last(APIView):
            def get(self, request, days):
                print(days)

# http://www.ietf.org/rfc/rfc2324.txt
class teapot(APIView):
    def get(self, request):
        json_result = "I'm a teapot."
        return Response(json_result, status=418)
        # return HttpResponse("I'm a teapot.", content_type="application/json", status=418)

        # Todo: Need  a class to handle user quality feedback, add entrey to sleep quality and reinsert label back to each feature entry
