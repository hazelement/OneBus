
import pandas as pd
import sqlite3
import os
import numpy as np
import requests
from zipfile import ZipFile
from io import BytesIO
import gc

import config
import util


#todo different city seems to have different data format, maybe keep useful ones only and line up data value and types

def update_all_database():
    config = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/city_url.config')

    city_codes = config['city'].values

    for city in city_codes:
        print "Garbage collection: ", gc.collect()
        print "unreachable garbage: ", gc.collect()
        _update_city_database(city)


def _update_city_database(city_province_country):

    print("updating database for " +city_province_country)
    print("downloading from transitfeed.com " +city_province_country)
    request = requests.get(config.read_city_url_from_config(city_province_country))
    z = ZipFile(BytesIO(request.content))
    print("download finished")
    
    file_names=['agency', 'shapes', 'stops', 'stop_times', 'routes']

    current_folder = os.path.dirname(os.path.realpath(__file__)) + "/"
    db_name = current_folder + "SQLData/" +city_province_country + ".sqlite"

    with sqlite3.connect(db_name) as con:
        for fname in file_names:
            print("processing " + fname)
            try:
                data = util.convert_csv_to_dataframe(z.open(fname + ".txt"))
                util.save_dataframe_to_db(data, fname, con)
            except KeyError:
                print(fname + " not in the data catalog")


        fname = 'calendar'
        print("processing " + fname)
        data = util.convert_csv_to_dataframe(z.open(fname + ".txt"))

        service_id_replacement=0
        if(type(data['service_id'].values[0]) is str): # convert service id to int if it is read in as string
            service_ids = np.unique(data['service_id'].values)
            service_id_replacement=1
            service_dict = {}

            count = 0
            for service_id in service_ids:
                service_dict[service_id] = count
                count+=1

            data.replace({"service_id": service_dict}, inplace=True)
            data[['service_id']]=data[['service_id']].astype(int)

        util.save_dataframe_to_db(data, fname, con)

        # maping service id string to integers in trips, route_id to intergers

        fname = 'trips'
        print("processing " + fname)
        data = util.convert_csv_to_dataframe(z.open(fname + ".txt"))

        if(service_id_replacement==1):
            data.replace({"service_id": service_dict}, inplace=True)
            data[['service_id']]=data[['service_id']].astype(int)

        util.save_dataframe_to_db(data, fname, con)



    print("finished")

if __name__ == "__main__":
    # update_all_database()
    # list = ["23:42:23", "32:01:32"]
    # _update_city_database('toronto_on_canada')
    _update_city_database('edmonton_ab_canada')
    _update_city_database('vancouver_bc_canada')

    #
    # print(convert_time_string_to_int(list))


