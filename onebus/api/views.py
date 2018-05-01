# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.shortcuts import render

from gtfs_tools import get_available_services, get_nearby_stops, get_following_stops
# Create your views here.

from django.http import HttpResponse


def query(request):
    # http://127.0.0.1:8000/api/query?lat=51.173569&lon=-114.118553&datetime=2018-04-29_18:47:05
    lat = float(request.GET['lat'])
    lon = float(request.GET['lon'])
    date_time = request.GET['datetime']

    datetime_object = datetime.strptime(date_time, '%Y-%m-%d_%H:%M:%S')

    # get available trips
    services = get_available_services(datetime_object.date())
    # print(services)

    # get nearby stops
    stops = get_nearby_stops(lat, lon)
    # print(stops)

    # get nearby trips from these stops
    following_stops = get_following_stops(stops, services, datetime_object)
    print(following_stops)


    # find POI that lies around these stops


    # get accessible POI, their trip_id, start_stop, end_stop, route_info, shape


    # construct response
    #
    # destination_name
    # start_stop : lat, lon, time, stop_name
    # end_stop: lat, lon, time, stop_name
    # shape:  before, during, after # before hop on bus, while on bus, after bus
    # route_number
    # route_headsign

    return HttpResponse("Success")