
import pandas as pd
import sqlite3
import os
import numpy as np


# todo add yelp api
# todo add yelp label on front page
# todo add function to download gtfs zip from transitfeed.com and dump it into database

def update_database(city_province_country):

    print("updating database for " +city_province_country)
    file_names=['agency', 'calendar_dates',
                'shapes', 'stop_times', 'stops']

    current_folder = os.path.dirname(os.path.realpath(__file__)) + "/"
    db_name = current_folder + "SQLData/" +city_province_country + ".sqlite"


    with sqlite3.connect(db_name) as con:
        for fname in file_names:
            print("processing " + fname)
            data = pd.read_csv(current_folder + 'RawData/' + fname +".txt")
            data.to_sql(fname, con, if_exists='replace')

        # maping service id string to integers in calendar
        fname = 'calendar'
        print("processing " + fname)
        data = pd.read_csv(current_folder + 'RawData/' + fname +".txt")

        service_ids = np.unique(data['service_id'].values)

        service_dict = {}

        for service_id in service_ids:
            service_dict[service_id] = len(service_dict)

        data.replace({"service_id": service_dict}, inplace=True)
        data[['service_id']]=data[['service_id']].astype(int)

        data.to_sql(fname, con, if_exists='replace')

        # maping service id string to integers in trips, route_id to intergers

        fname = 'trips'
        print("processing " + fname)
        data = pd.read_csv(current_folder + 'RawData/' + fname +".txt")
        data.replace({"service_id": service_dict}, inplace=True)
        data[['service_id']]=data[['service_id']].astype(int)

        data['route_id'] = data['route_id'].str.replace('-','0')
        data[['route_id']]=data[['route_id']].astype(int)

        data.to_sql(fname, con, if_exists='replace')


        # maping service id string to integers in trips, route_id to intergers

        fname = 'routes'
        print("processing " + fname)
        data = pd.read_csv(current_folder + 'RawData/' + fname +".txt")

        data['route_id'] = data['route_id'].str.replace('-','0')
        data[['route_id']]=data[['route_id']].astype(int)

        data.to_sql(fname, con, if_exists='replace')



    print("finished")

if __name__ == "__main__":
    update_database("calgary_ab_canada")



