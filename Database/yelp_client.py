
import oauth2
import six
import json

class Oauth1Authenticator(object):

    def __init__(
        self,
        consumer_key,
        consumer_secret,
        token,
        token_secret
    ):
        self.consumer = oauth2.Consumer(consumer_key, consumer_secret)
        self.token = oauth2.Token(token, token_secret)

    def sign_request(self, url, url_params={}):
        oauth_request = oauth2.Request(
            method="GET",
            url=url,
            parameters=url_params
        )
        oauth_request.update(
            {
                'oauth_nonce': oauth2.generate_nonce(),
                'oauth_timestamp': oauth2.generate_timestamp(),
                'oauth_token': self.token.key,
                'oauth_consumer_key': self.consumer.key
            }
        )
        oauth_request.sign_request(
            oauth2.SignatureMethod_HMAC_SHA1(),
            self.consumer,
            self.token
        )
        return oauth_request.to_url()


class Client(object):

    SEARCH_PATH = '/v2/search/'
    def __init__(self, authenticator):
        self.client = client
        self.authenticator = authenticator
        # self._error_handler = ErrorHandler()
        # self._define_request_methods()

    def _format_coordinates(
        self,
        latitude,
        longitude,
        accuracy,
        altitude,
        altitude_accuracy
    ):
        coord = '{0},{1}'.format(latitude, longitude)
        for field in (accuracy, altitude, altitude_accuracy):
            if field is not None:
                coord += ',' + str(field)
            else:
                break
        return coord


    def search_by_coordinates(
            self,
            latitude,
            longitude,
            accuracy=None,
            altitude=None,
            altitude_accuracy=None,
            **url_params
        ):
            """Make a request to the search endpoint by geographic coordinate.
            Specify a latitude and longitude with optional accuracy, altitude, and
            altitude_accuracy. More info at
            http://www.yelp.com/developers/documentation/v2/search_api#searchGC

            Args:
                latitude (float): Latitude of geo-point to search near.
                longitude (float): Longitude of geo-point to search near.
                accuracy (float): Optional accuracy of latitude, longitude.
                altitude (float): Optional altitude of geo-point to search near.
                altitude_accuracy (float): Optional accuracy of altitude.
                **url_params: Dict corresponding to search API params
                    https://www.yelp.ca/developers/documentation/v2/search_api#searchGP

            Returns:
                SearchResponse object that wraps the response.

            """
            url_params['ll'] = self._format_coordinates(
                latitude,
                longitude,
                accuracy,
                altitude,
                altitude_accuracy
            )

            return self.client._make_request(self.SEARCH_PATH, url_params)


    def sign_request(self, url, url_params={}):
            oauth_request = oauth2.Request(
                method="GET",
                url=url,
                parameters=url_params
            )
            oauth_request.update(
                {
                    'oauth_nonce': oauth2.generate_nonce(),
                    'oauth_timestamp': oauth2.generate_timestamp(),
                    'oauth_token': self.token.key,
                    'oauth_consumer_key': self.consumer.key
                }
            )
            oauth_request.sign_request(
                oauth2.SignatureMethod_HMAC_SHA1(),
                self.consumer,
                self.token
            )
            return oauth_request.to_url()

    def _make_request(self, path, url_params={}):
        url = 'https://{0}{1}?'.format(
            'api.yelp.com',
            six.moves.urllib.parse.quote(path.encode('utf-8'))
        )
        signed_url = self.authenticator.sign_request(url, url_params)
        return self._make_connection(signed_url)

    def _make_connection(self, signed_url):
        try:
            conn = six.moves.urllib.request.urlopen(signed_url, None)
        except six.moves.urllib.error.HTTPError as error:
            self._error_handler.raise_error(error)
        else:
            try:
                response = json.loads(conn.read().decode('UTF-8'))
            finally:
                conn.close()
            return response

if __name__ == "__main__":

    lat = 51.0454027
    lng = -114.05651890000001
    # query = 'chinese restaurant calgary'
    query = 'superstore'

    auth = Oauth1Authenticator( consumer_key='tImwuEyJbOKu9SyPce8BsA',
                            consumer_secret='YPeEHKUwtVj6FEI74FIvHqZz6h8',
                            token='1RKMAdt94utISAskO_hl_SkLCw9Iy2mP',
                            token_secret='CEMkBWE1_yzgOkqSenJgrPdWY58')

    client = Client(auth)

    params = {
        'term':query,
        'limit': '40',
        'radius_filter': '10000'
    }
    response = client.search_by_coordinates( lat, lng, params )

    print response