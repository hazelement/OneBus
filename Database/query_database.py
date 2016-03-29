import pandas as pd
import sqlite3
import numpy as np
import os
import datetime
import time

# from scipy.spatial.distance import cdist

import util
import config


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


def _find_current_serviceID(currDate, dayofthweek, con):

    sql_query="SELECT service_id FROM calendar WHERE start_date <= '{}' AND end_date >= {} and {}=1;".format(currDate, currDate, dayofthweek)

    df = pd.read_sql(sql_query, con)

    if(len(df)==0):  # if no service is available due to date problem, select any service id matches day of the week
        sql_query="SELECT service_id FROM calendar WHERE {}=1;".format(dayofthweek)
        df = pd.read_sql(sql_query, con)

    return df['service_id'].tolist()



def _find_near_trips(near_stops, service_id, currenttime, con):

    trips=[]

    st_trip_id=pd.read_sql("SELECT * FROM stop_times WHERE stop_id IN" + "(" + ','.join("{0}".format(x) for x in near_stops) + ") AND arrival_time>" +str(currenttime) + " ORDER BY arrival_time", con)
    trips_trip_id=pd.read_sql("SELECT * FROM trips WHERE service_id IN " +"(" + ','.join("{0}".format(x) for x in service_id) + ")", con)

    result = pd.merge(st_trip_id, trips_trip_id, on='trip_id')

    # print(result)
    # print(currenttime)

    # result = result[result['arrival_time']>currenttime]

    _ , unique_indices = np.unique(result['route_id'].values, return_index = True)

    trips = result['trip_id'].values[unique_indices]
    routes = result['route_id'].values[unique_indices]
    start_stops = result['stop_id'].values[unique_indices]


    return trips, routes, start_stops

def _find_stopID_along_strips(trips, con):

    # t2 = pd.read_sql("SELECT stop_id FROM stop_times WHERE trip_id IN " + "(" + ','.join("{0}".format(x) for x in trips) + ")" , con)
    # t = pd.read_sql("SELECT stop_id FROM stop_times WHERE trip_id IN " + "(" + ','.join("{0}".format(x) for x in trips) + ") GROUP BY trip_id" , con)
    # stop_ids = pd.read_sql("SELECT stop_id FROM stop_times WHERE trip_id IN " + "(" + ','.join("{0}".format(x) for x in trips) + ")" , con)['stop_id'].values

    all_stop_ids = pd.read_sql("SELECT stop_id,trip_id FROM stop_times WHERE trip_id IN " + "(" + ','.join("{0}".format(x) for x in trips) + ")" , con)

    stop_ids=[]
    for trip_id in trips:
        stop_id = all_stop_ids[all_stop_ids['trip_id']==trip_id]['stop_id'].values#  pd.read_sql("SELECT stop_id FROM stop_times WHERE trip_id=" + str(trip_id) , con)['stop_id'].values
        stop_ids.append(stop_id)

    # stop_ids = np.unique(stop_ids)

    return stop_ids

def find_accessiable_stops(lat, lng, ctime):
    '''
    find stops that is accessible from gps location through bus
    :param lat:
    :param lng:
    :param ctime: 'hh:mm:ss'
    :return: stops [[lat, lng], [lat, lng], [lat, lng]]
    '''

    current = ctime.split("|")
    current_day = current[0]
    current_time = current[1]

    city_code = config.read_city_code_from_config(lat, lng) # find city code
    print("city_code: " + city_code)
    db_location = os.path.dirname(os.path.realpath(__file__)) + '/SQLData/' +city_code + '.sqlite'

    with sqlite3.connect(db_location) as con:

        myLocation=np.array([[lat, lng]])

        with Timer("find stops around me"):
            sql_query = "SELECT stop_lat, stop_lon, stop_id from stops;"
            df_stops = pd.read_sql(sql_query, con)
            stop_loc=df_stops[['stop_lat', 'stop_lon']].as_matrix().astype(float)


            # calcValues=cdist(myLocation, stop_loc)[0]
            calcValues=util.distance_calc(myLocation, stop_loc)[0]

            nearestStopLocations=df_stops[calcValues<0.005]['stop_id'].values

        print nearestStopLocations


        with Timer("find today service id"):
            dt_today = datetime.datetime.strptime(current_day, "%Y-%m-%d") # yyyy-mm-dd to datetime object

            today = dt_today.strftime("%Y%m%d") #today = '20160124'
            dayofthweek = dt_today.strftime("%A").lower()  # saturday

            service_id = _find_current_serviceID(today, dayofthweek, con)

        gps_loc=[]

        with Timer("find trips from these stops"):
            currenttime=util.convert_time_string_to_int([current_time])[0]
            trips, routes, start_stopIDs=_find_near_trips(nearestStopLocations, service_id, currenttime, con)

        with Timer("find stops along trips"):
            stop_ids = _find_stopID_along_strips(trips, con)


        long_routes = []
        long_start_stopIDs = []
        long_stop_ids = np.array([])

        for i in range(0, len(stop_ids)):
            long_routes.extend([routes[i]] * len(stop_ids[i]))
            long_start_stopIDs.extend([start_stopIDs[i]] * len(stop_ids[i]))
            long_stop_ids = np.append(long_stop_ids, stop_ids[i])


        # lat_lng = df_stops[df_stops['stop_id'].isin(long_stop_ids)]
        # lat_lng = pd.read_sql("SELECT stop_lat, stop_lon FROM stops WHERE stop_id IN " + "(" + ','.join("{0}".format(x) for x in stop_ids) + ")", con)

        df = pd.DataFrame({'route_id': long_routes, 'start_stop_id': long_start_stopIDs, 'stop_id': long_stop_ids})# 'lat': lat_lng['stop_lat'], 'lon': lat_lng['stop_lon']})
        df = df.merge(df_stops, on='stop_id')
        # gps_loc=lat_lng[['stop_lat', 'stop_lon']].as_matrix().astype(float)

    # print(gps_loc)
    return df
    # return(np.array(gps_loc)), stop_ids, routes, start_stopIDs


if __name__ == "__main__":
    # lat = 43.7000  # toronto
    # lng = -79.4000
    lat = 51.135494 # calgary
    lng = -114.158389
    current_time = datetime.datetime.now()

    ctime = str(current_time.year) + "-" + str(current_time.month) + "-" + str(current_time.day) + "|" + str(current_time.hour) + ":" +str(current_time.minute) + ":" + str(current_time.second)
    ctime = "2016-03-28|08:10:32"
    print(find_accessiable_stops(lat, lng, ctime))

    # cProfile.run('foo() -s time')



