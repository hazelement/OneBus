
import pandas as pd
import sqlite3
import os
import numpy as np
import requests
from zipfile import ZipFile
from io import BytesIO

import config
import util


#todo different city seems to have different data format, maybe keep useful ones only and line up data value and types

def update_all_database():
    config = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/city_url.config')

    city_codes = config['city'].values

    city_codes = ['calgary_ab_canada']  #only update calgary

    for city in city_codes:
        _update_city_database(city)


def _update_city_database(city_province_country):

    #todo update all city database

    print("updating database for " +city_province_country)
    print("downloading from transitfeed.com " +city_province_country)
    request = requests.get(config.read_city_url_from_config(city_province_country))
    z = ZipFile(BytesIO(request.content))
    print("download finished")
    
    file_names=['agency', 'shapes', 'stops']


    current_folder = os.path.dirname(os.path.realpath(__file__)) + "/"
    db_name = current_folder + "SQLData/" +city_province_country + ".sqlite"


    with sqlite3.connect(db_name) as con:
        for fname in file_names:
            print("processing " + fname)
            data = pd.read_csv(z.open(fname + ".txt"))
            data.to_sql(fname, con, if_exists='replace')


        ''' convert stop times from string to integer '''

        fname = 'stop_times'
        print("processing " + fname)
        data = pd.read_csv(z.open(fname + ".txt"))

        if('shape_dist_traveled' in data):
            data.drop('shape_dist_traveled', axis=1, inplace=True)

        arrival_time = data['arrival_time'].values
        departure_time = data['arrival_time'].values

        arrival_time = util.convert_time_string_to_int(arrival_time)
        departure_time = util.convert_time_string_to_int(departure_time)

        data['arrival_time']=arrival_time
        data['departure_time']=departure_time

        data.to_sql(fname, con, if_exists='replace')

        ''' maping service id string to integers in calendar '''

        fname = 'calendar'
        print("processing " + fname)
        data = pd.read_csv(z.open(fname + ".txt"))



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

        data.to_sql(fname, con, if_exists='replace')

        ''' maping service id string to integers in trips, route_id to intergers '''

        fname = 'trips'
        print("processing " + fname)
        data = pd.read_csv(z.open(fname + ".txt"))

        if(service_id_replacement==1):
            data.replace({"service_id": service_dict}, inplace=True)
            data[['service_id']]=data[['service_id']].astype(int)

        route_id_replacement=0
        if(type(data['route_id'].values[0]) is str):
            route_id_replacement=1
            data['route_id'] = data['route_id'].str.replace('-','0')  # maybe need to find other special char
            data[['route_id']]=data[['route_id']].astype(int)

        data.to_sql(fname, con, if_exists='replace')


        ''' maping service id string to integers in routes, route_id to intergers '''

        fname = 'routes'
        print("processing " + fname)
        data = pd.read_csv(z.open(fname + ".txt"))

        if(route_id_replacement==1):
            data['route_id'] = data['route_id'].str.replace('-','0')
            data[['route_id']]=data[['route_id']].astype(int)

        data.to_sql(fname, con, if_exists='replace')



    print("finished")

if __name__ == "__main__":
    update_all_database()
    # list = ["23:42:23", "32:01:32"]
    # _update_city_database('toronto_on_canada')
    #
    # print(convert_time_string_to_int(list))


