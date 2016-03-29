
import numpy as np
# from scipy.spatial.distance import cdist
import datetime

import query_database
import query_api as api
import util
# todo return result should contain upcoming bus arrival time, bus shape from stop to destination, shape from my location to bus stop?, bus number
# todo update code to follow PEP8 format
# todo add city gps coordinates to city_url.config => automatically detect city from gps location and select database to use

def _result_filter_by_distance(stops, targets):
    """
    return index only
    :param stops: array of stops to reference from
    :param targets: array of targets to filter through
    :return:
    """

    # distance_matrix = cdist(stops, targets, 'euclidean')
    distance_matrix = util.distance_calc(stops, targets)

    min_target_distance = np.amin(distance_matrix, axis=0)
    threshold = 0.005

    # find targets are closest to stops
    target_mapping = min_target_distance<threshold

    # find stops that are closest to these targets
    stop_mapping = np.argmin(distance_matrix, axis=0)

    return target_mapping, stop_mapping[target_mapping] # selecting only stops that are closed to good targets


# def get_destinations(lat, lng, query, option):
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


    # gps_array, names, addresses = go_loc_list(lat, lng, query)  # Google
    # gps_array2, names2, addresses2 = fs_loc_list(lat, lng, query)  # Foursquare
    gps_array, names, addresses, image_url, yelp_url, review_count, rating_img_url = api.yelp_loc_list(lat, lng, query) #yelp results

    print("Number of raw destinations: " + str(len(names)))


    if(len(names)>0):
        # todo consider put this into dataframe, with repetitive stop_ids etc
        # stops, stop_ids, routes, start_stopIDs= query_database.find_accessiable_stops(lat, lng, ctime)
        df_stops = query_database.find_accessiable_stops(lat, lng, ctime)

        stop_gps = df_stops[['stop_lat', 'stop_lon']].as_matrix().astype(float)

        target_filter_index, stop_filter_index = _result_filter_by_distance(stop_gps, gps_array)

        dest_dict = {}

        # todo maybe we can use pandas here, consider move everything into query_database.py
        gps_array = gps_array[target_filter_index]
        names = names[target_filter_index]
        addresses = addresses[target_filter_index]
        image_url = image_url[target_filter_index]
        yelp_url = yelp_url[target_filter_index]
        review_count = review_count[target_filter_index]
        rating_img_url = rating_img_url[target_filter_index]

        start_stops = df_stops.ix[stop_filter_index]['start_stop_id'].values
        end_stops = df_stops.ix[stop_filter_index]['stop_id'].values



        print("Transit friendly results: " + str(len(names)))
        print(names)

        # print(names)
        # print(addresses)

        for i in range(0, len(gps_array)):
            dest_dict[names[i]]={"dest_name": names[i],
                                 "address": addresses[i],
                                 "lat": gps_array[i][0],
                                 "lng": gps_array[i][1],
                                 "image_url": image_url[i],
                                 "yelp_url": yelp_url[i],
                                 "review_count": review_count[i],
                                 "ratings_img": rating_img_url[i],
                                 "start_stop": start_stops[i],
                                 "end_stop": end_stops[i]}

        retVal={}
        retVal['results']=dest_dict
    else:
        retVal={}
        retVal['results']={}

    return retVal





if __name__ == "__main__":

    # toronto
    # lat = 43.7000
    # lng = -79.4000

    # calgary
    lat = 51.0454027
    lng = -114.05651890000001

    lat = 51.174280200000005
    lng = -114.121324

    # query = 'chinese restaurant calgary'
    query = 'restaurant'

    # gps, name, address = loc_list(lat, lng, stop_query)

    current_time = datetime.datetime.now()

    ctime = str(current_time.year) + "-" + str(current_time.month) + "-" +str(current_time.day) + "|" + str(current_time.hour) + ":" +str(current_time.minute) + ":" + str(current_time.second)
    # ctime = "2016-03-16|08:10:32"
    test = get_destinations(lat, lng, query, ctime)

    # test = yelp_loc_list(lat, lng, query)

    print test

    # print(gps)
    # print(name)
    # print(address)

    # fs_loc_list(51.0454027, -114.05651890000001, "japanese restaurant")
