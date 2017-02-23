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

@api_view(['GET'])
def temperature(request, days):
    if request.user.is_authenticated():
        r = queries.get_last_temperature(request, days)
        #print("type", type(r.data))
        json = JSONRenderer().render(r.data)
        stream = BytesIO(json)
        data = JSONParser().parse(stream)

        fig=plt.figure()
        ax=fig.add_subplot(111)

        ax.set_xlabel('Time')
        ax.set_ylabel('Heartrate')

        #fig.xlabel('Time')
        #fig.ylabel('Heartrate')

        timestamp=[]
        temp=[]

        for i in data:
            timestamp.append(datetime.strptime(i["date"], '%Y-%m-%dT%H:%M:%SZ'))
            temp.append(i['mean_temp'])

        if len(timestamp) != 0 and len(temp) != 0:
            ax.plot(timestamp, temp, '-')
            ax.xaxis.set_major_formatter(DateFormatter('%d/%m %H:%M:%S'))
            fig.autofmt_xdate()

            canvas=FigureCanvas(fig)
            response=HttpResponse(status=200, content_type='image/png')
            canvas.print_png(response)
            return response
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_401_UNAUTHORIZED)
