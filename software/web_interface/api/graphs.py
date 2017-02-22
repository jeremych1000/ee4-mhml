from django.http import HttpResponse

from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot
from pylab import *

import random, datetime, json, requests
from requests.auth import HTTPBasicAuth

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

from . import views, queries

def initial_test(request):
    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


def temperature(request, days):
    if request.user.is_authenticated():
        r = queries.get_last_temperature(request, days)
        #print("RRRRRRRRR", r, "type", type(r))
        json = JSONRenderer().render(r)

        print("dataaaaa", json, "TYPE", type(json))

    #
        #fig=Figure()
        #ax=fig.add_subplot(111)
        #x=[]
        #y=[]
        #now=datetime.datetime.now()
        #delta=datetime.timedelta(days=1)
        #for i in range(10):
        #    x.append(now)
        #    now+=delta
        #    y.append(random.randint(0, 1000))
        #ax.plot_date(x, y, '-')
        #ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        #fig.autofmt_xdate()
        #canvas=FigureCanvas(fig)
        #response=HttpResponse(content_type='image/png')
        #canvas.print_png(response)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)
