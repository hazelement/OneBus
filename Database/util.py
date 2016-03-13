import urllib
import json
import numpy as np
from scipy.spatial.distance import cdist
import stop_query
import config as cf

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator




def filter_by_distance(stops, targets):
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


def get_destinations(lat, lng, query, option):

    # return {'results': {'restaurant 1':{"dest_name": 'restaurant 1', "address":'address 1', "lat": 51.135494, "lng": -114.158389},
    #         'restaurant 2':{"dest_name": 'restaurant 2', "address":'address 2', "lat": 51.132494, "lng": -114.157389},
    #         'restaurant 3': {"dest_name":'restaurant 3', "address":'address 3', "lat": 51.131494, "lng": -114.155389}}}

    # gps_array, names, addresses = go_loc_list(lat, lng, query)  # Google

    # gps_array2, names2, addresses2 = fs_loc_list(lat, lng, query)  # Foursquare


    # yelp_loc_list
    gps_array, names, addresses = yelp_loc_list(lat, lng, query)

    # gps_array=np.concatenate((gps_array, gps_array2), axis=0)
    # names=np.concatenate((names, names2), axis=0)
    # addresses=np.concatenate((addresses, addresses2), axis=0)

    print("Number of raw destinations: " + str(len(names)))



    stops= stop_query.find_stops(lat, lng)

    filter_index = filter_by_distance(stops, gps_array)

    dest_dict = {}

    gps_array = gps_array[filter_index]
    names = names[filter_index]
    addresses = addresses[filter_index]


    print("Transit friendly results: " + str(len(names)))
    print(names)

    # print(names)
    # print(addresses)

    for i in range(0, len(gps_array)):
        dest_dict[names[i]]={"dest_name": names[i],
                                  "address": addresses[i],
                                  "lat": gps_array[i][0],
                                  "lng": gps_array[i][1]}

    retVal={}
    retVal['results']=dest_dict

    return retVal


def fetch_url(url):
    f = urllib.urlopen(url)
    response = json.loads(f.read())
    return response

def fs_loc_list(lat, lng, query):
    print("using four square")
    
    fs_secret=cf.read_api_config('fs_secret') 
    fs_client=cf.read_api_config('fs_client')

    srchquery="https://api.foursquare.com/v2/venues/search?near=calgary,ab&query="
    srchquery+=query
    srchquery+="&v=20150214&m=foursquare&client_secret=" + fs_secret + "&client_id=" + fs_client

               
    res = fetch_url(srchquery)
    #print res

    loc_list = []
    name = []
    address = []
    for i in range(len(res['response']['venues'])):
        lat=res['response']['venues'][i]['location']['lat']
        lng=res['response']['venues'][i]['location']['lng']
        name.append(res['response']['venues'][i]['name'])
        loc_list.append([lat, lng])
        address.append(res['response']['venues'][i]['location']['formattedAddress'][0])

    gps_array = np.array(loc_list)
    name = np.array(name)
    address = np.array(address)
    return gps_array, name, address



def go_loc_list(lat, lng, query):
    # lat = 51.135494
    # lng = -114.158389
    # query = 'japanese restaurant'

    print("using google")

    query += " Calgary AB"

    loc_p = 'location'+str(lat)+','+str(lng)
    qry_list = query.strip().split(' ')
    qry_p = 'query=' + qry_list[0]
    for i in qry_list[1:]:
        qry_p += '+'
        qry_p += i
    rad_p = 'radius=10000'
   
    api_key = "key=" + cf.read_api_config('google')  # yyc Calgary key google places api web service


    srch = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
    srch += qry_p + '&'
    srch += loc_p + '&'
    srch += rad_p + '&'
    srch += api_key

    res = fetch_url(srch)

    # return res

    # print(res)
    loc_list = []
    name = []
    address = []
    for loc in res['results']:
        lat = loc['geometry']['location']['lat']
        lng = loc['geometry']['location']['lng']
        loc_list.append([lat, lng])
        name.append(loc['name'])
        address.append(loc['formatted_address'])

    while('next_page_token' in res and len(name)<40):


        page_token = "pagetoken=" + res['next_page_token']
        srch = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
        # srch += qry_p + '&'
        srch += page_token +"&"
        srch += api_key

        res = fetch_url(srch)

        for loc in res['results']:
            lat = loc['geometry']['location']['lat']
            lng = loc['geometry']['location']['lng']
            loc_list.append([lat, lng])
            name.append(loc['name'])
            address.append(loc['formatted_address'])


    gps_array = np.array(loc_list)
    name = np.array(name)
    address = np.array(address)

    # print name
    # print address
    return gps_array, name, address





def yelp_loc_list(lat, lng, query):
    print("using yelp")
    # lat = 51.135494
    # lng = -114.158389
    # query = 'japanese restaurant'

    auth = Oauth1Authenticator( consumer_key=cf.read_api_config('yelp_consumer_key'),
                                consumer_secret=cf.read_api_config('yelp_consumer_secret'),
                                token=cf.read_api_config('yelp_token'),
                                token_secret=cf.read_api_config('yelp_token_secret'))

    client = Client(auth)

    # params = {
    #     'term':query,
    #     'limit': '40',
    #     'radius_filter': '10000'
    # }
    response = client.search_by_coordinates( lat, lng, accuracy=None, altitude=None,  altitude_accuracy=None, term=query )


    loc_list = []
    name = []
    address = []

    for loc in response.businesses:
        lat = loc.location.coordinate.latitude
        lng = loc.location.coordinate.longitude
        loc_list.append([lat, lng])
        name.append(loc.name)
        address.append(' '.join(loc.location.display_address))


    gps_array = np.array(loc_list)
    name = np.array(name)
    address = np.array(address)

    print name
    # print address
    return gps_array, name, address

if __name__ == "__main__":



    lat = 51.0454027
    lng = -114.05651890000001
    # query = 'chinese restaurant calgary'
    query = 'superstore'

    # gps, name, address = loc_list(lat, lng, stop_query)

    # test = get_destinations(lat, lng, query, "google")

    test = yelp_loc_list(lat, lng, query)

    print test

    # print(gps)
    # print(name)
    # print(address)

    # fs_loc_list(51.0454027, -114.05651890000001, "japanese restaurant")
