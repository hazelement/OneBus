import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onebus.settings")
django.setup()

from datetime import datetime

from api.models import Stop, Route, Trip, Shape

from api.repo import get_available_services, get_nearby_stops, get_following_stops, get_start_stop
from api.utils.rectangle_gen import get_search_rectangles
from api.utils.poi_api import yelp_rec_batch
from api.utils.math_tools import result_filter_by_distance


def search_query(lat, lon, date_time, search_word):
    datetime_object = datetime.strptime(date_time, '%Y-%m-%d_%H:%M:%S')

    # get available trips
    services = get_available_services(datetime_object.date())
    # print(services)

    # get nearby stops
    nearby_stops = get_nearby_stops(lat, lon)
    # print(stops)

    # get nearby trips from these stops
    following_stops = get_following_stops(nearby_stops, services, datetime_object)
    print(following_stops)

    # get POI from queries and around stops
    stop_lat_lons = following_stops[['stop_lat', 'stop_lon']].values

    # generate search rectangles, POI query will be based on these rectangles
    search_rectangles = get_search_rectangles(stop_lat_lons)
    print(search_rectangles)

    poi_result = yelp_rec_batch(search_rectangles, search_word)
    print(poi_result)

    poi_lat_lons = poi_result[['lat', 'lon']]

    # find POI that lies around these stops
    # get accessible POI, their trip_id, start_stop, end_stop, route_info, shape
    stop_mapping, poi_mapping = result_filter_by_distance(stop_lat_lons, poi_lat_lons)

    selected_pois = poi_result[poi_mapping]
    print(selected_pois)

    selected_stops = following_stops.ix[stop_mapping]
    print(selected_stops)

    # construct response
    # get start stop from trip_id and accessible stops

    # construct route information for each poi
    stop_infos = []
    for index, row in selected_stops.iterrows():
        print(index, row)
        trip_id = row['trip_id']
        trip = Trip(trip_id=trip_id)
        start_stop = get_start_stop(trip, nearby_stops)
        end_stop = Stop(stop_id=row["stop_id"])
        route = Route(route_id=row['route_id'])
        shape = Shape(shape_id=trip.shape_id)


        # todo get shape based on start/end stop

        stop_infos.append({ "start_stop":
                                {
                                    "start_stop_name": start_stop.stop_id.stop_name,
                                    "start_stop_time": start_stop.arrival_time ,
                                    "start_stop_lat": start_stop.stop_id.stop_lat,
                                    "start_stop_lon": start_stop.stop_id.stop_lon
                                },
                            "end_stop":
                                {
                                    "end_stop_name": end_stop.stop_name,
                                    "end_stop_time": row["time"],
                                    "end_stop_lat": end_stop.stop_lat,
                                    "end_stop_lon": end_stop.stop_lon
                                },
                            "route_info":
                                {
                                    "shape": "asdfwef",
                                    "route_name": route.route_short_name
                                }

        })


    print("gogo")


    # use stop id to get stop names


    # use route id to get route information


    # use trip id to get shape



    # destination: name, hours, etc
    # start_stop : lat, lon, time, stop_name
    # end_stop: lat, lon, time, stop_name
    # shape:  before, during, after # before hop on bus, while on bus, after bus
    # route_number
    # route_headsign


if __name__=="__main__":
    lat = 51.173569
    lon = -114.118553
    date_time = "2018-04-29_18:47:05"

    search_query(lat, lon, date_time, "restaurant")

