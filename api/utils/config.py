import pandas as pd
import os
import numpy as np

import math_tools
# from scipy.spatial.distance import cdist

# superseded
def read_route_id_process_key(city):

    config = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/city_url.config')
    return config[config['city']==city].values[0][4]

# superseded
def read_city_url_from_config(city):
    config = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/city_url.config')
    return config[config['city']==city].values[0][1]

# superseded
def read_city_code_from_config(lat, lng):
    config = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/city_url.config')

    lat_lng=config[['lat', 'lng']].as_matrix().astype(float)

    print(lat, lng)
    # calcValues=cdist([[lat, lng]],lat_lng)[0]
    calcValues=math_tools.distance_calc([[lat, lng]], lat_lng)[0]
    city_index = np.argmin(calcValues, axis=0)

    city_code = config.ix[city_index]['city']

    return city_code

def read_api_config(item):
    config = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/api.config')
    return config[config['item']==item].values[0][1]


if __name__ == "__main__":
    lat = 51.135494
    lng = -114.158389

    print(read_city_code_from_config(lat, lng))

