# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.http import HttpResponse

from utils.onebus_query import search_query
# Create your views here.


# TODO encapusulate query search into classes with POIQuery class injection (maybe use factory pattern)
# TODO encapsulate POI search into classes
# TODO test search functionality with online POI search
# TODO setup test script for POIQuery, API testing
# TODO POI search caching in database

def query(request):
    # http://127.0.0.1:8000/api/query?lat=51.173569&lon=-114.118553&datetime=2018-04-29_18:47:05&search_word=food
    lat = float(request.GET['lat'])
    lon = float(request.GET['lon'])
    date_time = request.GET['datetime']
    search_word = request.GET['search_word']

    search_query(lat, lon, date_time, search_word)

    return HttpResponse("Success")