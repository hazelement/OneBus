# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.shortcuts import render

from gtfs_tools import get_available_services, get_nearby_stops, get_nearby_trips
# Create your views here.

from django.http import HttpResponse


def query(request):
    # http://127.0.0.1:8000/api/query?lat=51.173569&lon=-114.118553&datetime=2018-04-29_18:47:05
    lat = float(request.GET['lat'])
    lon = float(request.GET['lon'])
    date_time = request.GET['datetime']

    datetime_object = datetime.strptime(date_time, '%Y-%m-%d_%H:%M:%S')

    services = get_available_services(datetime_object.date())
    print(services)

    stops = get_nearby_stops(lat, lon)
    print(stops)

    get_nearby_trips(stops, services, datetime_object)

    return HttpResponse("Success")