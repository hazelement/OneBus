# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def query(request):
    lat = float(request.GET['lat'])  # => [39]
    lon = float(request.GET['lon'])  # => [137]



    return HttpResponse("Success")