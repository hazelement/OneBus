# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.shortcuts import render

from gtfs_tools import get_services
# Create your views here.

from django.http import HttpResponse


def query(request):
    lat = float(request.GET['lat'])
    lon = float(request.GET['lon'])
    date_time = request.GET['datetime']

    datetime_object = datetime.strptime(date_time, '%Y-%m-%d_%H:%M:%S')

    services = get_services(datetime_object.date())

    print(services)

    return HttpResponse("Success")