from django.http import HttpResponse
from django.utils.six import BytesIO

from pylab import *
from datetime import datetime
import random, json

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.decorators import api_view

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from matplotlib import pyplot as plt

from . import views, queries


def initial_test(request):
    fig = Figure()
    ax = fig.add_subplot(111)
    x = []
    y = []
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now += delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


@api_view(['GET'])
def simple_graph(request, feature, days=None, start=None, end=None):
    if request.user.is_authenticated():
        if feature == 'heartrate':
            serializer = queries.heartrate(request, days)
        elif feature == 'rr':
            serializer = queries.rr(request, days)
        elif feature == 'gsr':
            serializer = queries.gsr(request, days)
        elif feature == 'temperature':
            serializer = queries.temperature(request, days)
        elif feature == 'acceleration':
            serializer = queries.acceleration(request, days)
        # elif feature == 'sleep_duration':
        #    serializer = queries.sleep_duration(request, days)
        else:
            pass


        if feature == "heartrate":
            r = queries.heartrate(request, days)
        # print("type", type(r.data))
        json = JSONRenderer().render(r.data)
        stream = BytesIO(json)
        data = JSONParser().parse(stream)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.set_xlabel('Time')
        ax.set_ylabel('Heartrate')

        # fig.xlabel('Time')
        # fig.ylabel('Heartrate')

        timestamp = []
        temp = []

        for i in data:
            timestamp.append(datetime.strptime(i["date"], '%Y-%m-%dT%H:%M:%SZ'))
            temp.append(i['mean_hr'])

        if len(timestamp) != 0 and len(temp) != 0:
            ax.plot(timestamp, temp, '-')
            ax.xaxis.set_major_formatter(DateFormatter('%d/%m %H:%M:%S'))
            fig.autofmt_xdate()

        canvas = FigureCanvas(fig)
        response = HttpResponse(status=200, content_type='image/png')
        if request.method == 'GET' and 'dl' in request.GET:
            response['Content-Disposition'] = 'attachment; filename="%s.png"' % (
                'heartrate_last_' + days + '_days_from_' + str(
                    datetime.strptime(data[0]["date"], '%Y-%m-%dT%H:%M:%SZ')))
        canvas.print_png(response)
        # clear and close plots to prevent memory problems
        fig.clf()
        plt.close(fig)
        return response

    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def rr(request, days):
    if request.user.is_authenticated():
        r = queries.rr(request, days)
        # print("type", type(r.data))
        json = JSONRenderer().render(r.data)
        stream = BytesIO(json)
        data = JSONParser().parse(stream)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.set_xlabel('Time')
        ax.set_ylabel('RR')

        # fig.xlabel('Time')
        # fig.ylabel('Heartrate')

        timestamp = []
        temp = []

        for i in data:
            timestamp.append(datetime.strptime(i["date"], '%Y-%m-%dT%H:%M:%SZ'))
            temp.append(i['mean_rr'])

        if len(timestamp) != 0 and len(temp) != 0:
            ax.plot(timestamp, temp, '-')
            ax.xaxis.set_major_formatter(DateFormatter('%d/%m %H:%M:%S'))
            fig.autofmt_xdate()

        canvas = FigureCanvas(fig)
        response = HttpResponse(status=200, content_type='image/png')
        if request.method == 'GET' and 'dl' in request.GET:
            response['Content-Disposition'] = 'attachment; filename="%s.png"' % (
                'rr_last_' + days + '_days_from_' + str(datetime.strptime(data[0]["date"], '%Y-%m-%dT%H:%M:%SZ')))
        canvas.print_png(response)
        # clear and close plots to prevent memory problems
        fig.clf()
        plt.close(fig)
        return response
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def gsr(request, days):
    if request.user.is_authenticated():
        r = queries.gsr(request, days)
        # print("type", type(r.data))
        json = JSONRenderer().render(r.data)
        stream = BytesIO(json)
        data = JSONParser().parse(stream)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.set_xlabel('Time')
        ax.set_ylabel('GSR')

        # fig.xlabel('Time')
        # fig.ylabel('Heartrate')

        timestamp = []
        temp = []

        for i in data:
            timestamp.append(datetime.strptime(i["date"], '%Y-%m-%dT%H:%M:%SZ'))
            temp.append(i['mean_gsr'])

        if len(timestamp) != 0 and len(temp) != 0:
            ax.plot(timestamp, temp, '-')
            ax.xaxis.set_major_formatter(DateFormatter('%d/%m %H:%M:%S'))
            fig.autofmt_xdate()

        canvas = FigureCanvas(fig)
        response = HttpResponse(status=200, content_type='image/png')
        if request.method == 'GET' and 'dl' in request.GET:
            response['Content-Disposition'] = 'attachment; filename="%s.png"' % (
                'gsr_last_' + days + '_days_from_' + str(datetime.strptime(data[0]["date"], '%Y-%m-%dT%H:%M:%SZ')))
        canvas.print_png(response)
        # clear and close plots to prevent memory problems
        fig.clf()
        plt.close(fig)
        return response
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def temperature(request, days):
    if request.user.is_authenticated():
        r = queries.temperature(request, days)
        # print("type", type(r.data))
        json = JSONRenderer().render(r.data)
        stream = BytesIO(json)
        data = JSONParser().parse(stream)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.set_xlabel('Time')
        ax.set_ylabel('Temperature')

        # fig.xlabel('Time')
        # fig.ylabel('Heartrate')

        timestamp = []
        temp = []

        for i in data:
            timestamp.append(datetime.strptime(i["date"], '%Y-%m-%dT%H:%M:%SZ'))
            temp.append(i['mean_temp'])

        if len(timestamp) != 0 and len(temp) != 0:
            ax.plot(timestamp, temp, '-')
            ax.xaxis.set_major_formatter(DateFormatter('%d/%m %H:%M:%S'))
            fig.autofmt_xdate()

        canvas = FigureCanvas(fig)
        response = HttpResponse(status=200, content_type='image/png')
        if request.method == 'GET' and 'dl' in request.GET:
            response['Content-Disposition'] = 'attachment; filename="%s.png"' % (
                'temperature_last_' + days + '_days_from_' + str(
                    datetime.strptime(data[0]["date"], '%Y-%m-%dT%H:%M:%SZ')))
        canvas.print_png(response)
        # clear and close plots to prevent memory problems
        fig.clf()
        plt.close(fig)
        return response
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def acceleration(request, days):
    if request.user.is_authenticated():
        r = queries.acceleration(request, days)
        # print("type", type(r.data))
        json = JSONRenderer().render(r.data)
        stream = BytesIO(json)
        data = JSONParser().parse(stream)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.set_xlabel('Time')
        ax.set_ylabel('Acceleration')

        # fig.xlabel('Time')
        # fig.ylabel('Heartrate')

        timestamp = []
        temp = []

        for i in data:
            timestamp.append(datetime.strptime(i["date"], '%Y-%m-%dT%H:%M:%SZ'))
            temp.append(i['mean_acc'])

        if len(timestamp) != 0 and len(temp) != 0:
            ax.plot(timestamp, temp, '-')
            ax.xaxis.set_major_formatter(DateFormatter('%d/%m %H:%M:%S'))
            fig.autofmt_xdate()

        canvas = FigureCanvas(fig)
        response = HttpResponse(status=200, content_type='image/png')
        if request.method == 'GET' and 'dl' in request.GET:
            response['Content-Disposition'] = 'attachment; filename="%s.png"' % (
                'acceleration_last_' + days + '_days_from_' + str(
                    datetime.strptime(data[0]["date"], '%Y-%m-%dT%H:%M:%SZ')))
        canvas.print_png(response)
        # clear and close plots to prevent memory problems
        fig.clf()
        plt.close(fig)
        return response
    return Response(status=status.HTTP_401_UNAUTHORIZED)
