import json
import multiprocessing
import time
import urllib
from abc import abstractmethod, ABCMeta
from functools import partial
from multiprocessing.pool import ThreadPool

import numpy as np
import pandas as pd
from googleplaces import GooglePlaces
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

import config as cf
from math_tools import measure

ABC = ABCMeta('ABC', (object,), {'__slots__': ()})

# TODO implement POI search using base classes for Google, Yelp and FourSquare

yelp_api_config = cf.read_api_config('yelp_consumer_api_key')
google_places_api_key = cf.read_api_config('google_places_api_key')


class Timer:
    """
    Timer for profiling
    """

    def __init__(self, fnname):
        self.name = fnname

    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start
        print(self.name + " took " + str(self.interval) + " sec.")


class AbstractPOIQuery(ABC):
    """
    Abstract POI query class, all POI based search query should substract this class
    """

    # todo add search by coordinate abstract method
    @abstractmethod
    def query_rec_batch(self, rec_array, query):
        """
        search batched rectangle with a query
        :param rec_array: list rectanges to search on [[sw_lat, sw_lon, ne_lat, ne_lon], [sw_lat, sw_lon, ne_lat, ne_lon], ...]
        :param query: str, query string
        :return: list of BasePOI instance
        """
        pass


class BasePOI(ABC):
    """
    Base POI class, all POI class should substract this class
    """

    def __init__(self, name, address, url, rating, lat, lon):
        """

        :param name: unicode, name of this place
        :param address: unicode, address of this place
        :param image_url: unicode, image link of this place
        :param url: unicode, website of this place
        :param rating: float, out of 1
        :param lat: float, latitude of this place
        :param lon: float, longitude of this place
        """

        assert isinstance(name, unicode)
        assert isinstance(address, unicode)
        assert isinstance(rating, float)
        assert isinstance(lat, float)
        assert isinstance(lon, float)

        self.name = name
        self.address = address
        self.url = url
        self.rating = rating
        self.lat = lat
        self.lon = lon

    def to_dict(self):
        """
        Convert to dictionary
        :return:
        """
        return {'name': self.name,
                'address': self.address,
                'url': self.url,
                'rating': self.rating,
                'poi_lat': self.lat,
                'poi_lon': self.lon}


class YelpPOI(BasePOI):
    def __init__(self, name, address, image_url, url, review_count, lat, lon):
        BasePOI.__init__(self, name, address, url, int(review_count), float(lat), float(lon))


class YelpPOIQuery(AbstractPOIQuery):
    def __init__(self):
        self.client = Client(yelp_api_config)

    def _get_yelp(self, rectange, query):
        """
        get yelp result
        :param rectangle:  [sw_lat, sw_lon, ne_lat, ne_lon]
        :return: pandas dataframe
        """

        df = pd.DataFrame(
            columns=['name', 'address', 'image_url', 'yelp_url', 'review_count', 'ratings_img_url', 'lat', 'lon'])

        response = self.client.search_by_bounding_box(rectange[0], rectange[1], rectange[2], rectange[3], term=query,
                                                      limit='20', sort='0')
        # response = client.search_by_coordinates( lat, lng, accuracy=None, altitude=None,  altitude_accuracy=None, term=query, limit='20', radius_filter=radius_filter, sort='0', offset=str(i*20)) # meter
        for loc in response.businesses:
            df.loc[len(df) + 1] = [loc.name,
                                   ' '.join(loc.location.display_address),
                                   loc.image_url, loc.url,
                                   loc.review_count,
                                   loc.rating_img_url,
                                   loc.location.coordinate.latitude,
                                   loc.location.coordinate.longitude]

        df[['review_count']] = df[['review_count']].astype(int)

        return df

    def query_rec_batch(self, rec_array, query):

        data = self._get_yelp(rec_array, query)

        result = []
        for index, row in data.iterrows():
            result.append(
                YelpPOI(row['name'], row['address'], row['image_url'], row['url'], row['review_count'], row['lat'],
                        row['lon']))

        return result


class GooglePOI(BasePOI):
    def __init__(self, name, address, url, rating, lat, lon):
        BasePOI.__init__(self, name, address, url, rating, float(lat), float(lon))


class GooglePOIQuery(AbstractPOIQuery):
    def __init__(self):
        self.google_places = GooglePlaces(google_places_api_key)

    def _get_google(self, rectange, query):
        """
        get yelp result
        :param rectangle:  [sw_lat, sw_lon, ne_lat, ne_lon]
        :return: pandas dataframe
        """

        lat_lng = {'lat': ((float)(rectange[0] + rectange[2])) / 2.0,
                   'lng': ((float)(rectange[1] + rectange[3])) / 2.0}
        radius = measure(*rectange) / 2

        query_result = self.google_places.nearby_search(
            lat_lng=lat_lng, keyword=query,
            radius=radius)

        result = []
        for loc in query_result.places:

            loc.get_details() # todo maybe do local caching based on place id
            result.append(GooglePOI(loc.name,
                                    loc.formatted_address,
                                    loc.website,
                                    (float(loc.rating)) / 5, # google's full score is 5 star
                                    float(loc.geo_location['lat']),
                                    float(loc.geo_location['lng'])))

        return result

    def query_rec_batch(self, rec_array, query):
        result = []
        for rec in rec_array:
            result.extend(self._get_google(rec, query))

        return result


if __name__ == "__main__":
    lat = 51.0454027
    lng = -114.05651890000001
    query = "restaurant"

    google_poi_query = GooglePOIQuery()
    print(google_poi_query.query_rec_batch([[51.0454027, -114.05652, 51.0230, -114.123]], query))
