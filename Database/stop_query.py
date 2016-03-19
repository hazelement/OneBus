import pandas as pd
import sqlite3
import numpy as np
import os

import datetime
import update_database
from scipy.spatial.distance import cdist

import time


class Timer:
    def __init__(self, fnname):
        self.name = fnname

    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start
        print(self.name + " took " + str(self.interval) + " sec.")


def currentServiceID(currDate, dayofthweek, con):  # currentServiceID(today, dayofthweek)

    sql_query="SELECT service_id FROM calendar where start_date <= '{}' AND end_date >= {} and {}=1;".format(currDate, currDate, dayofthweek)

    df = pd.read_sql(sql_query, con)

    return df['service_id'].tolist()



def find_near_trips(near_stops, service_id, currenttime, con):

    trips=[]

    st_trip_id=pd.read_sql("SELECT * FROM stop_times WHERE stop_id IN" + "(" + ','.join("{0}".format(x) for x in near_stops) + ") and arrival_time>" +str(currenttime), con) # todo do sorting
    trips_trip_id=pd.read_sql("SELECT * FROM trips WHERE service_id IN " +"(" + ','.join("{0}".format(x) for x in service_id) + ")", con)

    result = pd.merge(st_trip_id, trips_trip_id, on='trip_id')

    print(result)
    print(currenttime)

    # result = result[result['arrival_time']>currenttime]

    _ , unique_indices = np.unique(result['route_id'].values, return_index = True)

    trips = np.unique(result['trip_id'].values[unique_indices])


    return trips

def find_stopids_along_strips(trips, con):

    stop_ids = pd.read_sql("SELECT stop_id FROM stop_times WHERE trip_id IN " + "(" + ','.join("{0}".format(x) for x in trips) + ")" , con)['stop_id'].values

    stop_ids = np.unique(stop_ids)

    return stop_ids

def find_stops_around(lat, lng, ctime):
    '''
    find stops that is accessible from gps location through bus
    :param lat:
    :param lng:
    :param ctime: 'hh:mm:ss'
    :return: stops [[lat, lng], [lat, lng], [lat, lng]]
    '''

    db_location = os.path.dirname(os.path.realpath(__file__)) + '/SQLData/calgary_ab_canada.sqlite'

    with sqlite3.connect(db_location) as con:

        myLocation=np.array([[lat, lng]])

        with Timer("find stops around me"):
            sql_query = "SELECT stop_lat, stop_lon, stop_id from stops;"
            df_stops = pd.read_sql(sql_query, con)
            stop_loc=df_stops[['stop_lat', 'stop_lon']].as_matrix().astype(float)


            calcValues=cdist(myLocation, stop_loc)[0]

            nearestStopLocations=df_stops[calcValues<0.005]['stop_id'].values #stop_loc[calcValues<0.005]

        print nearestStopLocations

        ## /yyyy/mm/d format


        with Timer("find today service id"):
            dt_today = datetime.datetime.today()

            today = dt_today.strftime("%Y%m%d") #today = '20160124'
            dayofthweek = dt_today.strftime("%A").lower()  # saturday


            service_id = currentServiceID(today, dayofthweek, con)

        gps_loc=[]

        with Timer("find trips from these stops"):
            currenttime=update_database.convert_time_string_to_int([ctime])[0]
            trips=find_near_trips(nearestStopLocations,service_id,currenttime,con)

        with Timer("find stops along trips"):
            stop_ids = find_stopids_along_strips(trips, con)

            lat_lng = df_stops[df_stops['stop_id'].isin(stop_ids)]
            # lat_lng = pd.read_sql("SELECT stop_lat, stop_lon FROM stops WHERE stop_id IN " + "(" + ','.join("{0}".format(x) for x in stop_ids) + ")", con)

            gps_loc=lat_lng[['stop_lat', 'stop_lon']].as_matrix().astype(float)



    # print(gps_loc)

    return(np.array(gps_loc))

def foo():
    lat = 51.135494
    lng = -114.158389
    current_time = datetime.datetime.now()
    time = str(current_time.hour) + ":" +str(current_time.minute) + ":" + str(current_time.second)
    print(find_stops_around(lat, lng, time))

if __name__ == "__main__":
    foo()

    # cProfile.run('foo() -s time')



