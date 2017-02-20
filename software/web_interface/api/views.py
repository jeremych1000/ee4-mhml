from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from datetime import datetime
import os, re, json, random

from . import csv_functions
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
        print ("exist ", exist)

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

        # call ML insert_from_api
        # from MLBlock.views
        # concac_data = [mean_hr, std_hr, mean_rr, std_rr, mean_gsr, std_gsr, mean_temp, std_temp, mean_acc, outcome]
        # insert_from_api(username, date, concac_data)
        return Response(json_result, status=status.HTTP_200_OK)



class on_off(APIView):
    def get(self, request):
        json = random.getrandbits(1)
        return Response(json, status=status.HTTP_200_OK)


#http://www.ietf.org/rfc/rfc2324.txt
class teapot(APIView):
    def get(self, request):
        json_result = "I'm a teapot."
        return Response(json_result, status=418)
        #return HttpResponse("I'm a teapot.", content_type="application/json", status=418)