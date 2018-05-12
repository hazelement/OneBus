# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.http import HttpResponse

from utils.onebus_query import search_query
# Create your views here.


def query(request):
    # http://127.0.0.1:8000/api/query?lat=51.173569&lon=-114.118553&datetime=2018-04-29_18:47:05
    lat = float(request.GET['lat'])
    lon = float(request.GET['lon'])
    date_time = request.GET['datetime']
    search_word = request.GET['search_word']

    search_query(lat, lon, date_time, search_word)

    return HttpResponse("Success")