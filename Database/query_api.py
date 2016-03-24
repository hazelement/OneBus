
import urllib
import json
import numpy as np

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

import config as cf

def _fetch_url(url):
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


    res = _fetch_url(srchquery)
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

    res = _fetch_url(srch)

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

        res = _fetch_url(srch)

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
    '''

    :param lat:
    :param lng:
    :param query:
    :return: np.arrays loc_list, name, address, image_url, yelp_url, review_count, rating_img_url
    '''
    print("using yelp")

    auth = Oauth1Authenticator( consumer_key=cf.read_api_config('yelp_consumer_key'),
                                consumer_secret=cf.read_api_config('yelp_consumer_secret'),
                                token=cf.read_api_config('yelp_token'),
                                token_secret=cf.read_api_config('yelp_token_secret'))
    client = Client(auth)

    loc_list = []
    name = []
    address = []
    image_url = []
    yelp_url = []
    review_count = []
    rating_img_url = []

    for i in range(0, 2):
        response = client.search_by_coordinates( lat, lng, accuracy=None, altitude=None,  altitude_accuracy=None, term=query, limit='20', radius_filter='10000', sort='1', offset=str(i*20)) # meter
        for loc in response.businesses:
            loc_list.append([loc.location.coordinate.latitude, loc.location.coordinate.longitude])
            name.append(loc.name)
            address.append(' '.join(loc.location.display_address))
            image_url.append(loc.image_url)
            yelp_url.append(loc.url)
            review_count.append(loc.review_count)
            rating_img_url.append(loc.rating_img_url)

    loc_list = np.array(loc_list)
    name = np.array(name)
    address = np.array(address)
    image_url = np.array(image_url)
    yelp_url = np.array(yelp_url)
    review_count = np.array(review_count)
    rating_img_url = np.array(rating_img_url)

    print(len(name))
    print name
    # print address
    return loc_list, name, address, image_url, yelp_url, review_count, rating_img_url

if __name__=="__main__":
    lat = 51.0454027
    lng = -114.05651890000001
    query = "restaurant"
    yelp_loc_list(lat, lng, query)