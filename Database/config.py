import pandas as pd
import os

def read_api_config(item):
    config = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/api.config')
    return config[config['item']==item].values[0][1]


if __name__ == "__main__":
    print(read_api_config('fs_secret'))
