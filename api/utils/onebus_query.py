import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onebus.settings")
django.setup()

from api.repo import *
from api.utils.rectangle_gen import get_search_rectangles, get_distance, Point
from api.utils.poi_api import GooglePOIQuery
from api.utils.math_tools import result_filter_by_distance
from api.utils.polyline_en_de_coder import encode_coords


def search_query(lat, lon, date_time, search_word):
    """
    Given a lot and lon coordinate, date_time string, and search keyword
    return list of POI that can arrive within one bus ride
    :param lat: latitude, float
    :param lon: longitude, float
    :param date_time: string, '%Y-%m-%d_%H:%M:%S'
    :param search_word: string, search word
    :return:
    """
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

    # get stop coordinates from trips
    stop_lat_lons = following_stops[['stop_lat', 'stop_lon']].values

    # generate search rectangles along these stops, POI query will be based on these rectangles
    search_rectangles = get_search_rectangles(stop_lat_lons)
    # print(search_rectangles)

    # perform POI query to find POI within these rectanges
    poi_result = GooglePOIQuery().query_rec_batch(search_rectangles, search_word)
    # poi_result = yelp_rec_batch(search_rectangles, search_word)
    poi_result = pd.DataFrame.from_records([x.to_dict() for x in poi_result])
    print(poi_result)

    # POI lat and lon
    poi_lat_lons = poi_result[['poi_lat', 'poi_lon']]

    # find POI that lies around these stops, filter out those are too far
    # get accessible POI, their trip_id, start_stop, end_stop, route_info, shape
    stop_mapping, poi_mapping = result_filter_by_distance(stop_lat_lons, poi_lat_lons)

    selected_pois = poi_result[poi_mapping]
    print(selected_pois)

    selected_stops = following_stops.ix[stop_mapping]
    print(selected_stops)

    # construct response
    # get start stop from trip_id and accessible stops

    selected_pois.reset_index(drop=True, inplace=True)
    selected_stops.reset_index(drop=True, inplace=True)
    combined = pd.concat([selected_pois, selected_stops], axis=1)

    # construct route information for each poi
    poi_bus_infos = []
    for index, row in combined.iterrows():

        # todo add search engine ID, yelp, google, foursquare etc
        print(index, row)
        trip_id = row['trip_id']
        print(trip_id)
        trip = Trip.objects.filter(trip_id=trip_id).first()
        print(trip.shape_id)
        start_stop = get_start_stop(trip, nearby_stops)
        end_stop = Stop.objects.filter(stop_id=row["stop_id"]).first()
        route = Route.objects.filter(route_id=row['route_id']).first()
        shapes = get_shape_points(trip.shape.shape_id)

        print(shapes)

        # get shape based on start and end stop
        # calculate start shape point, and end shape point
        start_ind = 0
        start_shape_dist = get_distance(Point(shapes[0].shape_pt_lat, shapes[0].shape_pt_lon),
                                        Point(start_stop.stop.stop_lat, start_stop.stop.stop_lon))
        end_ind = 0
        end_shape_dist = get_distance(Point(shapes[0].shape_pt_lat, shapes[0].shape_pt_lon),
                                      Point(end_stop.stop_lat, end_stop.stop_lon))
        for i in range(len(shapes)):
            shape = shapes[i]
            new_start_distance = get_distance(Point(shape.shape_pt_lat, shape.shape_pt_lon),
                                              Point(start_stop.stop.stop_lat, start_stop.stop.stop_lon))
            if new_start_distance < start_shape_dist:
                start_shape_dist = new_start_distance
                start_ind = i

            new_end_distance = get_distance(Point(shape.shape_pt_lat, shape.shape_pt_lon),
                                            Point(end_stop.stop_lat, end_stop.stop_lon))
            if new_end_distance < end_shape_dist:
                end_shape_dist = new_end_distance
                end_ind = i

        # encode points into Google-encoded polyline string
        shape_points = shapes[start_ind:end_ind + 1]
        encoded = encode_coords([Point(item.shape_pt_lat, item.shape_pt_lon) for item in shape_points])

        poi_bus_infos.append({"start_stop":
            {
                "start_stop_name": start_stop.stop.stop_name,
                "start_stop_time": start_stop.arrival_time,
                "start_stop_lat": start_stop.stop.stop_lat,
                "start_stop_lon": start_stop.stop.stop_lon
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
                    "route_name": route.route_short_name
                },
            "shape": encoded,
            "poi": {
                "lat": row['poi_lat'],
                "lon": row['poi_lon'],
                "address": row['address'],
                'name': row['name'],
                'url': row['url'],
                'rating': row['rating']
            }

        })

    return poi_bus_infos


if __name__ == "__main__":

    lat = 51.173569
    lon = -114.118553
    date_time = "2018-04-29_18:47:05"

    print(search_query(lat, lon, date_time, "restaurant"))
