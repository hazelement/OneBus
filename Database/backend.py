
import numpy as np
from scipy.spatial.distance import cdist
import datetime

import query_database
import query_api as api


# todo return result should contain upcoming bus arrival time, bus shape from stop to destination, shape from my location to bus stop?, bus number
# todo update code to follow PEP8 format

def _result_filter_by_distance(stops, targets):
    '''
    return index only
    :param stops: array of stops to reference from
    :param targets: array of targets to filter through
    :return:
    '''

    map_distance = cdist(stops, targets, 'seuclidean')

    min_target_distance = np.amin(map_distance, axis=0)

    threshold = 0.08

    return min_target_distance<threshold


# def get_destinations(lat, lng, query, option):
def get_destinations(lat, lng, query, ctime):
    '''
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
    '''


    # gps_array, names, addresses = go_loc_list(lat, lng, query)  # Google
    # gps_array2, names2, addresses2 = fs_loc_list(lat, lng, query)  # Foursquare
    gps_array, names, addresses, image_url, yelp_url, review_count, rating_img_url = api.yelp_loc_list(lat, lng, query) #yelp results

    print("Number of raw destinations: " + str(len(names)))

    if(len(names)>0):
        stops= query_database.find_stops_around(lat, lng, ctime)

        result_filter_index = _result_filter_by_distance(stops, gps_array)

        dest_dict = {}

        gps_array = gps_array[result_filter_index]
        names = names[result_filter_index]
        addresses = addresses[result_filter_index]
        image_url = image_url[result_filter_index]
        yelp_url = yelp_url[result_filter_index]
        review_count = review_count[result_filter_index]
        rating_img_url = rating_img_url[result_filter_index]


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
                                 "ratings_img": rating_img_url[i]}

        retVal={}
        retVal['results']=dest_dict
    else:
        retVal={}
        retVal['results']={}

    return retVal





if __name__ == "__main__":



    lat = 51.0454027
    lng = -114.05651890000001
    # query = 'chinese restaurant calgary'
    query = 'superstore'

    # gps, name, address = loc_list(lat, lng, stop_query)

    current_time = datetime.datetime.now()

    time = str(current_time.hour) + ":" +str(current_time.minute) + ":" + str(current_time.second)
    test = get_destinations(lat, lng, query, time)

    # test = yelp_loc_list(lat, lng, query)

    print test

    # print(gps)
    # print(name)
    # print(address)

    # fs_loc_list(51.0454027, -114.05651890000001, "japanese restaurant")
