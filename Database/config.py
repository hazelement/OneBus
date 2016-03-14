import pandas as pd
import os

def read_transitfeed_config(city):
    config = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/city_url.config')
    return config[config['city']==city].values[0][1]

def read_api_config(item):
    config = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/api.config')
    return config[config['item']==item].values[0][1]


if __name__ == "__main__":
    #print(read_api_config('fs_secret'))
    print(read_transitfeed_config('calgary_ab_canada'))
