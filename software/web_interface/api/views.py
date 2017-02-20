from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from datetime import datetime
from collections import deque
import os, csv, re, json, random


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

        exist = raw_data.check_duplicate(raw_data.file_prefix + date + ".csv", username)
        print ("exist ", exist)

        if not exist:
            try:
                # print (path, "---", final_path)
                raw_data.csv_insert_header(path, final_path,
                                           ["Time", "HR", "RR", "Mode", "GSR", "SkinT", "AccX", "AccY", "AccZ",
                                            "outcome"])
            except IOError:
                messages.error(request, 'error while inserting header')

            last_time = datetime.utcfromtimestamp(0).strftime("%d/%m/%y %H:%M:%S")
        else:
            last_row = raw_data.get_last_row(final_path)[0]
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
                    success = raw_data.csv_append(final_path, [
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

    def csv_append(filename, data):
        with open(filename, 'a', newline='') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(data)
            return True
        return IOError

    def csv_insert_header(path, filename, header):
        os.makedirs(path, exist_ok=True)
        open(filename, 'a', newline='').close()
        with open(filename, 'w', newline='') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(header)
            return True
        return IOError

    def get_last_row(filename):
        with open(filename, 'r', newline='') as f:
            try:
                lastrow = deque(csv.reader(f), 1)[0]
            except IndexError:  # empty file
                lastrow = None
            return lastrow

    def check_duplicate(name, username=None):
        if username is None:
            path = os.path.join(os.path.join(settings.MEDIA_ROOT, 'data'), name)
        else:
            path = os.path.join(os.path.join(os.path.join(settings.MEDIA_ROOT, 'data'), username), name)
        # print("check duplidate Path is ", path)
        return os.path.isfile(path)


class on_off(APIView):
    def get(self, request):
        if random.getrandbits(1):
            json = "ON"
        else:
            json = "OFF"
        return Response(json, status=status.HTTP_200_OK)


#http://www.ietf.org/rfc/rfc2324.txt
class teapot(APIView):
    def get(self, request):
        json_result = "I'm a teapot."
        return Response(json_result, status=418)
        #return HttpResponse("I'm a teapot.", content_type="application/json", status=418)