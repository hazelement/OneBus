
import numpy as np
import datetime

import query_database
import query_api as api
import util


# todo return result should contain upcoming bus arrival time

def get_shape_gps(city_code, trip_id, start_stop, end_stop):

    trip_id = int(trip_id)
    start_stop = int(start_stop)
    end_stop = int(end_stop)

    return query_database.find_shape_lat_lng(city_code, trip_id, start_stop, end_stop)


def get_destinations(lat, lng, query, ctime):
    """
    return filter destination results
    :param lat:
    :param lng:
    :param query: search text
    :param ctime: "hh:mm:ss"
    :return:{ 'results':  {'restaurant 1':{"dest_name": 'restaurant 1', "address":'address 1', "lat": 51.135494, "lng": -114.158389, *param},
                            'restaurant 2':{"dest_name": 'restaurant 2', "address":'address 2', "lat": 51.132494, "lng": -114.157389, *param},
                            'restaurant 3': {"dest_name":'restaurant 3', "address":'address 3', "lat": 51.131494, "lng": -114.155389, *param}
                          }
            }
    """
    lat = float(lat)
    lng = float(lng)
    # df_targets = api.yelp_loc_list(lat, lng, query)

    # print("Number of raw destinations: " + str(len(df_targets)))


    df_stops, city_code = query_database.find_accessiable_stops(lat, lng, ctime)

    if(len(df_stops)>0):

        stop_gps = df_stops[['stop_lat', 'stop_lon']].as_matrix().astype(float)

        all_route_ids = ",".join([str(x) for x in np.unique(df_stops['route_id'].values).tolist()])

        batch_to_search = np.append(stop_gps[::5], [stop_gps[-1]], axis=0)
        df_targets = api.yelp_batch(batch_to_search, query)  # search around every 5 stops
        print("Number of raw destinations: " + str(len(df_targets)))
        if(len(df_targets)>0):

            target_gps = df_targets[['lat', 'lon']].as_matrix().astype(float)

            stop_filter_index, target_filter_index = util.result_filter_by_distance(stop_gps, target_gps, False)

            dest_dict = {}

            # filter out data

            df_targets = df_targets[target_filter_index]
            df_stops = df_stops.ix[stop_filter_index]

            print("Transit friendly results: " + str(len(df_targets)))
            print(df_targets['name'].values)


            # trip heading, stop id location
            for i in range(0, len(df_targets)):
                dest_dict[df_targets.iloc[i]['name']]={"dest_name": df_targets.iloc[i]['name'],
                                                       "address": df_targets.iloc[i]['address'],
                                                       "lat": float(df_targets.iloc[i]['lat']),
                                                       "lng": float(df_targets.iloc[i]['lon']),
                                                       "image_url": df_targets.iloc[i]['image_url'],
                                                       "yelp_url": df_targets.iloc[i]['yelp_url'],
                                                       "review_count": int(df_targets.iloc[i]['review_count']),
                                                       "ratings_img": df_targets.iloc[i]['ratings_img_url'],
                                                       "start_stop": int(df_stops.iloc[i]['start_stop_id']),
                                                       "start_stop_time": int(df_stops.iloc[i]['start_stop_time']),
                                                       "start_stop_name": df_stops.iloc[i]['start_stop_name'],
                                                       "end_stop": int(df_stops.iloc[i]['stop_id']),
                                                       "end_stop_time": int(df_stops.iloc[i]['stop_time']),
                                                       "end_stop_name": df_stops.iloc[i]['stop_name'],
                                                       "trip_id": int(df_stops.iloc[i]['trip_id']),
                                                       "trip_headsign": df_stops.iloc[i]['trip_headsign'],
                                                       "route_id": int(df_stops.iloc[i]['route_id']),
                                                       "city_code": city_code}

            retVal={}
            retVal['results']=dest_dict
        else:
            retVal={}
            retVal['results']={}

        retVal['routes']=all_route_ids

    else:
        retVal={}
        retVal['results']={}
        retVal['routes']=""


    return retVal


if __name__ == "__main__":

    # toronto
    lat = 43.7000
    lng = -79.4000

    # calgary
    # lat = 51.0454027
    # lng = -114.05651890000001

    # lat = 51.174280200000005
    # lng = -114.121324
    #
    # lat = 37.983730
    # lng = -122.524635  # san franciso

    # lat = 51.1382372
    # lng = -114.1371632

    # lat = 51.0794168
    # lng = -114.1348398

    # query = 'chinese restaurant calgary'
    query = 'tea'

    # gps, name, address = loc_list(lat, lng, stop_query)

    current_time = datetime.datetime.now()

    ctime = str(current_time.year) + "-" + str(current_time.month) + "-" +str(current_time.day) + "|" + str(current_time.hour) + ":" +str(current_time.minute) + ":" + str(current_time.second)
    # ctime = "2016-03-16|08:10:32
    ctime = "2016-04-17|09:30:00"
    test = get_destinations(lat, lng, query, ctime)

    # test = yelp_loc_list(lat, lng, query)

    print test

    # print(gps)
    # print(name)
    # print(address)

    # fs_loc_list(51.0454027, -114.05651890000001, "japanese restaurant")
