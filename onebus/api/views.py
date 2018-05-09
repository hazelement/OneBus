# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.http import HttpResponse

from api.utils.gtfs_tools import get_available_services, get_nearby_stops, get_following_stops
from api.utils.rectangle_gen import get_search_rectangles
from api.utils.poi_api import yelp_rec_batch
from api.utils.math_tools import result_filter_by_distance
# Create your views here.


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

    # get POI from queries and around stops
    stop_lat_lons = following_stops[['stop_lat', 'stop_lon']].values

    # generate search rectangles, POI query will be based on these rectangles
    search_rectangles = get_search_rectangles(stop_lat_lons)
    print(search_rectangles)

    poi_result = yelp_rec_batch(search_rectangles, 'restaurant')
    print(poi_result)

    poi_lat_lons = poi_result[['lat', 'lon']]

    stop_mapping, poi_mapping = result_filter_by_distance(stop_lat_lons, poi_lat_lons)

    selected_pois = poi_result[poi_mapping]
    print(selected_pois)

    selected_stops = following_stops.ix[stop_mapping]
    print(selected_stops)


    # find POI that lies around these stops


    # get accessible POI, their trip_id, start_stop, end_stop, route_info, shape


    # construct response
    #
    # destination: name, hours, etc
    # start_stop : lat, lon, time, stop_name
    # end_stop: lat, lon, time, stop_name
    # shape:  before, during, after # before hop on bus, while on bus, after bus
    # route_number
    # route_headsign

    return HttpResponse("Success")