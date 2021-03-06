from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from django_cron import CronJobBase, Schedule

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

import newML.functions
from newML import models as ml_model
from datetime import datetime, date, timedelta
from cal import read as cal_read, import_events
from myaccount import models

import os, re, json, random, pickle, requests, numpy as np

from . import csv_functions, serializers, queries

from MLBlock.views import insert_from_api


def csrf(request):
    return render(request, "personal/blank.html")

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'api.mycronjob'    # a unique code

    def do(self):
        requests.options('http://sleepify.zapto.org/api/dummy/')

class dummy(APIView):
    def post(self, request):
        json_data = json.loads(request.body.decode("utf-8"))
        print("Dummy DEBUG: ", json_data)
        return Response(json_data, status=status.HTTP_200_OK)

class random_number(APIView):
    def get(self, request):
        result = random.getrandbits(1)
        return Response(result, status=status.HTTP_200_OK)


class raw_data(APIView):
    file_prefix = "MSBand2_ALL_data_"

    def post(self, request):
        # print("raw_data_post", request)
        json_data = json.loads(request.body.decode("utf-8"))
        # print("DEBUG: ", json_data)

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
            if last_row == "Time":
                last_time = datetime.utcfromtimestamp(0).strftime("%d/%m/%y %H:%M:%S")
            else:
                last_time = datetime.strptime(last_row, '%d/%m/%y %H:%M:%S').strftime("%d/%m/%y %H:%M:%S")

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
        if settings.DEBUG_API:
            print("RT DEBUG: ", json_data)
        username = json_data['username']
        data = json_data["data"]
        # print('Last timestamp data in json ', data[-1]["timestamp"])
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
        temp = np.mean(newML.functions.getTempProfile(username))
        json_result["temp"] = temp
        if outcome == True:
            json_result["quality"] = "1"
        else:
            json_result["quality"] = "0"
        print("RT RETURN ", json_result)
        return Response(json_result, status=status.HTTP_200_OK)


class userFeedback(APIView):
    def post(self, request):
        json_data = json.loads(request.body.decode("utf-8"))
        if settings.DEBUG_API:
            print("UF DEBUG: ", json_data)
        newML.functions.labelInsertion(json_data)
        return Response(status=status.HTTP_200_OK)


class stats():
    class last(APIView):
        def get(self, request, feature, days):
            days = int(days)
            if request.user.is_authenticated():
                if feature == 'mean_hr':
                    serializer = queries.heartrate(request, days)
                elif feature == 'mean_rr':
                    serializer = queries.rr(request, days)
                elif feature == 'mean_gsr':
                    serializer = queries.gsr(request, days)
                elif feature == 'mean_temp':
                    serializer = queries.temperature(request, days)
                elif feature == 'mean_acc':
                    serializer = queries.acceleration(request, days)
                # elif feature == 'sleep_duration':
                #    serializer = queries.sleep_duration(request, days)
                else:
                    return Response(status=status.HTTP_204_NO_CONTENT)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

    class date_range(APIView):
        def get(self, request, feature, start, end):
            # print(start, end)
            start = datetime.strptime(start, '%Y-%m-%d')
            end = datetime.strptime(end, '%Y-%m-%d')
            ret = newML.functions.getFeatureInRange(request.user, start, end)

            if feature == 'mean_hr':
                serializer = serializers.FeatureEntrySerializer.mean_hr(ret, many=True)
            elif feature == 'mean_rr':
                serializer = serializers.FeatureEntrySerializer.mean_rr(ret, many=True)
            elif feature == 'mean_gsr':
                serializer = serializers.FeatureEntrySerializer.mean_gsr(ret, many=True)
            elif feature == 'mean_temp':
                serializer = serializers.FeatureEntrySerializer.mean_temp(ret, many=True)
            elif feature == 'mean_acc':
                serializer = serializers.FeatureEntrySerializer.mean_acc(ret, many=True)
            # elif feature == 'sleep_duration':
            #    serializer = serializers.FeatureEntrySerializer.sleep_duration(ret, many=True)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.data, status=status.HTTP_200_OK)


class get_cal_events(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        cal_events = cal_read.get_cal_events(request.user.username)
        return Response(cal_events, status=status.HTTP_200_OK)

class import_cal_events(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        days = 1
        exception_list = import_events.import_all(days)
        if len(exception_list) == 0:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"exceptions": exception_list}, status=status.HTTP_400_BAD_REQUEST)

class pushy_token(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        json_ret = {}

        if request.user.is_authenticated:
            json_data = json.loads(request.body.decode("utf-8"))
            username = json_data['username']
            token = json_data['token']

            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                json_ret["status"] = "fail"
                json_ret["reason"] = "User doesn't exit"
                return Response(json_ret, status=status.HTTP_400_BAD_REQUEST)

            try:
                models.PushyToken.objects.create(
                    user=user,
                    token=token,
                )

                json_ret["status"] = "success"
                json_ret["reason"] = "Successfully added to database"
                return Response(json_ret, status=status.HTTP_200_OK)
            except IntegrityError:
                pushy_obj = models.PushyToken.objects.get(user=user)
                pushy_obj.token = token
                try:
                    pushy_obj.full_clean()
                except ValidationError as e:
                    json_ret["status"] = "fail"
                    json_ret["reason"] = str(e.message_dict)
                    return Response(json_ret, status=status.HTTP_400_BAD_REQUEST)
                json_ret["status"] = "success"
                json_ret["reason"] = "Successfully updated"
                pushy_obj.save()
            return Response(json_ret, status=status.HTTP_200_OK)
        else:
            json_ret["status"] = "fail"
            json_ret["reason"] = "Please login"
            return Response(json_ret, status=status.HTTP_401_UNAUTHORIZED)


# http://www.ietf.org/rfc/rfc2324.txt
class teapot(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        print(request.META)
        print("adsfasfdadfa", request.META['HTTP_AUTHORIZATION'], request.META['CONTENT_TYPE'])

        json_result = "I'm a teapot."
        return Response(json_result, status=418)
