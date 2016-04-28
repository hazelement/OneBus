import pandas as pd
import sqlite3
import numpy as np
import os
import datetime
import time

from rdp import rdp

import util
import config
import polyline_en_de_coder as pl


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


def find_shape_lat_lng(city_code, trip_id, start_stop, end_stop):
    """
    find the shape points between start_stop, end_stop, along trip_id
    :param trip_id:
    :param start_stop:
    :param end_stop:
    :return:
    """
    print("retrieving shape info")

    db_location = os.path.dirname(os.path.realpath(__file__)) + '/SQLData/' +city_code + '.sqlite'

    with sqlite3.connect(db_location) as con:
        sql_query = "SELECT shape_id FROM trips WHERE trip_id=" + str(trip_id)
        shape_id = pd.read_sql(sql_query, con)['shape_id'].values[0]

        sql_query = "SELECT shape_pt_lat,shape_pt_lon FROM shapes WHERE shape_id=" + str(shape_id) + " ORDER BY shape_pt_sequence"
        shape = pd.read_sql(sql_query, con)
        shape_lat_lng = shape[['shape_pt_lat', 'shape_pt_lon']].as_matrix().astype(float)

        # is group by inroder of start stop and end stop
        sql_query = "SELECT stop_lat,stop_lon FROM stops WHERE stop_id IN (" + str(start_stop) + "," + str(end_stop) +") GROUP BY stop_id"
        gps_data =pd.read_sql(sql_query, con)[['stop_lat', 'stop_lon']].as_matrix().astype(float)

        start_lat_lng = np.array([gps_data[0]])
        end_lat_lng = np.array([gps_data[1]])

        # old approach
        # sql_query = "SELECT stop_lat,stop_lon FROM stops WHERE stop_id=" + str(start_stop)
        # start_lat_lng =pd.read_sql(sql_query, con)[['stop_lat', 'stop_lon']].as_matrix().astype(float)
        #
        #
        # sql_query = "SELECT stop_lat,stop_lon FROM stops WHERE stop_id=" + str(end_stop)
        # end_lat_lng =pd.read_sql(sql_query, con)[['stop_lat', 'stop_lon']].as_matrix().astype(float)

        start_loc = np.argmin(util.distance_calc(start_lat_lng, shape_lat_lng), axis=1)[0]
        end_loc = np.argmin(util.distance_calc(end_lat_lng, shape_lat_lng), axis=1)[0]

        lower = min(start_loc, end_loc)
        upper = max(start_loc, end_loc)

        shape_lat_lng = shape.ix[lower:upper][['shape_pt_lat', 'shape_pt_lon']].as_matrix().astype(float)

        shape_lat_lng_small = rdp(shape_lat_lng, epsilon=0.000002)  # reduce size using Ramer-Douglas-Peucker algorithm

        df = pd.DataFrame(shape_lat_lng_small, columns=['lat', 'lng'])

    tuples = [tuple(x) for x in df.values]

    encoded = pl.encode_coords(tuples)
    print(encoded)
    return encoded



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
            sql_query = "SELECT stop_lat, stop_lon, stop_id, stop_name from stops;"
            df_stops = pd.read_sql(sql_query, con)
            stop_loc=df_stops[['stop_lat', 'stop_lon']].as_matrix().astype(float)

            _, location_mapping = util.result_filter_by_distance(myLocation, stop_loc, True)
            nearestStopLocations = df_stops.ix[location_mapping]['stop_id'].values

        print nearestStopLocations

        if(len(nearestStopLocations) == 0):
            return [], city_code


        with Timer("find today service id"):
            dt_today = datetime.datetime.strptime(current_day, "%Y-%m-%d") # yyyy-mm-dd to datetime object

            today = dt_today.strftime("%Y%m%d") #today = '20160124'
            dayofthweek = dt_today.strftime("%A").lower()  # saturday

            service_id = _find_current_service_id(today, dayofthweek, con)

        with Timer("find trips from these stops"):
            currenttime=util.convert_time_string_to_int([current_time])[0]
            trip_ids, routes, start_stop_ids, start_stop_times, trip_headsign, df_trips=_find_near_trips(nearestStopLocations, service_id, currenttime, con)

        with Timer("find stops along trips"):
            stop_ids, stop_times = _find_stop_id_along_strips(trip_ids, start_stop_ids, con)

        with Timer("generate dataframe"):
            long_routes = []

            long_start_stop_ids = []
            long_start_stop_times = []
            long_start_stop_names = []

            long_stop_ids = []
            long_stop_times = []
            # long_stop_ids = np.array([])
            # long_stop_times = np.array([])
            long_stop_names = []

            long_trips = []
            long_trips_headsign = []

            for i in range(0, len(stop_ids)):
                long_routes.extend([routes[i]] * len(stop_ids[i]))

                long_trips.extend([trip_ids[i]] * len(stop_ids[i]))
                long_trips_headsign.extend([trip_headsign[i]] * len(stop_ids[i]))

                long_start_stop_ids.extend([start_stop_ids[i]] * len(stop_ids[i]))
                long_start_stop_times.extend([start_stop_times[i]] * len(stop_times[i]))
                long_start_stop_names.extend([df_stops[df_stops['stop_id']==start_stop_ids[i]]['stop_name'].values[0]] * len(stop_ids[i]))

                # long_stop_ids = np.append(long_stop_ids, stop_ids[i])
                # long_stop_times = np.append(long_stop_times, stop_times[i])
                long_stop_ids.extend(stop_ids[i].tolist())
                long_stop_times.extend(stop_times[i].tolist())

            df = pd.DataFrame({'route_id': long_routes,
                               'start_stop_id': long_start_stop_ids,
                               'start_stop_time': long_start_stop_times,
                               'start_stop_name': long_start_stop_names,
                               'stop_id': long_stop_ids,
                               'stop_time': long_stop_times,
                               'trip_id': long_trips,
                               'trip_headsign': long_trips_headsign
                               })

            df = df.merge(df_stops, on='stop_id')

            df = _convert_route_id_to_route_short_name(df, con)
            try:
                df[['route_id']] = df[['route_id']].astype(int)
            except:
                pass
            df[['start_stop_id']] = df[['start_stop_id']].astype(int)
            df[['stop_id']] = df[['stop_id']].astype(int)
            df[['start_stop_time']] = df[['start_stop_time']].astype(int)
            df[['stop_time']] = df[['stop_time']].astype(int)

    return df, city_code


def _convert_route_id_to_route_short_name(df, con):

    sql_query = "SELECT route_id,route_short_name FROM routes"
    route_df = pd.read_sql(sql_query, con)
    route_df[['route_id']] = route_df[['route_id']].astype(int)

    # mapping = route_df.to_dict("records")
    mapping = dict(zip(route_df['route_id'], route_df['route_short_name']))

    df[['route_id']] = df[['route_id']].astype(int)

    try:
        df.replace({'route_id': mapping}, inplace=True)
    except Exception, e:
        print(e)
        pass

    return df


def _find_current_service_id(currDate, dayofthweek, con):

    try:
        sql_query = "SELECT service_id FROM calendar WHERE start_date <= '{}' AND end_date >= {} and {}=1;".format(currDate, currDate, dayofthweek)
        df1 = pd.read_sql(sql_query, con)
    except:
        df1 = pd.DataFrame(columns=['service_id'])

    try:
        sql_query = "SELECT service_id FROM calendar_dates WHERE date = '{}' AND exception_type=1;".format(currDate, currDate, dayofthweek)
        df2 = pd.read_sql(sql_query, con)
    except:
        df2 = pd.DataFrame(columns=['service_id'])

    try:
        sql_query = "SELECT service_id FROM calendar_dates WHERE date = '{}' AND exception_type=2;".format(currDate, currDate, dayofthweek)
        df3 = pd.read_sql(sql_query, con)
    except:
        df3 = pd.DataFrame(columns=['service_id'])

    df = pd.merge(df1, df2, on='service_id', how='outer')

    mask = df['service_id'].isin(df3['service_id'].values)
    df = df[~mask]


    #
    # try:
    #     sql_query="SELECT service_id FROM calendar WHERE start_date <= '{}' AND end_date >= {} and {}=1 ".format(currDate, currDate, dayofthweek)
    #     sql_query+="UNION SELECT service_id FROM calendar_dates WHERE date = '{}' AND exception_type=1 ".format(currDate, currDate, dayofthweek)
    #     sql_query+="EXCEPT SELECT service_id FROM calendar_dates WHERE date = '{}' AND exception_type=2;".format(currDate, currDate, dayofthweek)
    #
    #     df = pd.read_sql(sql_query, con)
    #
    #
    # except Exception, e:
    #     sql_query="SELECT service_id FROM calendar WHERE start_date <= '{}' AND end_date >= {} and {}=1;".format(currDate, currDate, dayofthweek)
    #     df = pd.read_sql(sql_query, con)
    #     print(e)
    if(len(df)==0):  # if no service is available due to date problem, select any service id matches day of the week
        try:
            print("proper service id not available, using rough service id instead.")
            sql_query="SELECT service_id FROM calendar WHERE {}=1;".format(dayofthweek)
            df = pd.read_sql(sql_query, con)
        except Exception, e:
            print(e)
            pass

    return df['service_id'].tolist()

def _find_current_service_id_bak(currDate, dayofthweek, con):

    sql_query="SELECT service_id FROM calendar WHERE start_date <= '{}' AND end_date >= {} and {}=1;".format(currDate, currDate, dayofthweek)

    df = pd.read_sql(sql_query, con)

    if(len(df)==0):  # if no service is available due to date problem, select any service id matches day of the week
        sql_query="SELECT service_id FROM calendar WHERE {}=1;".format(dayofthweek)
        df = pd.read_sql(sql_query, con)

    return df['service_id'].tolist()


def _find_near_trips(near_stops, service_id, currenttime, con):

    trips=[]

    st_trip_id=pd.read_sql("SELECT trip_id,stop_id,arrival_time FROM stop_times WHERE stop_id IN" + "(" + ','.join("{0}".format(x) for x in near_stops) + ") AND arrival_time>" +str(currenttime) + " ORDER BY arrival_time", con)
    trips_trip_id=pd.read_sql("SELECT trip_id,route_id,trip_headsign FROM trips WHERE service_id IN " +"(" + ','.join("{0}".format(x) for x in service_id) + ")", con)

    # this one performance is slow
    # sql = "SELECT t.trip_id, st.stop_id, t.route_id FROM stop_times st, trips t " + \
    #       "WHERE st.stop_id IN (" + ','.join("{0}".format(x) for x in near_stops) + ") " + \
    #       "AND st.arrival_time>" + str(currenttime) + " "\
    #       "AND st.trip_id = t.trip_id " + \
    #       "AND t.service_id IN " +"(" + ','.join("{0}".format(x) for x in service_id) + ")" + " " + \
    #       "ORDER BY st.arrival_time"



    result = pd.merge(st_trip_id, trips_trip_id, on='trip_id')
    # result2 = pd.read_sql(sql, con)

    _ , unique_indices = np.unique(result['route_id'].values, return_index = True)

    trips = result['trip_id'].values[unique_indices]
    routes = result['route_id'].values[unique_indices]
    start_stops = result['stop_id'].values[unique_indices]
    start_stop_times = result['arrival_time'].values[unique_indices]
    trip_headsign = result['trip_headsign'].values[unique_indices]

    df_trips = result['trip_id'].values[unique_indices]


    return trips, routes, start_stops, start_stop_times, trip_headsign, df_trips


def _find_stop_id_along_strips(trips, start_stop_ids, con):

    # t2 = pd.read_sql("SELECT stop_id FROM stop_times WHERE trip_id IN " + "(" + ','.join("{0}".format(x) for x in trips) + ")" , con)
    # t = pd.read_sql("SELECT stop_id FROM stop_times WHERE trip_id IN " + "(" + ','.join("{0}".format(x) for x in trips) + ") GROUP BY trip_id" , con)
    # stop_ids = pd.read_sql("SELECT stop_id FROM stop_times WHERE trip_id IN " + "(" + ','.join("{0}".format(x) for x in trips) + ")" , con)['stop_id'].values

    all_stop_ids = pd.read_sql("SELECT stop_id,trip_id,arrival_time FROM stop_times WHERE trip_id IN " + "(" + ','.join("{0}".format(x) for x in trips) + ")" , con)

    stop_ids=[]
    stop_times=[]

    for i in range(0, len(trips)):
        trip_id = trips[i]
        start_stop_id = start_stop_ids[i]

        stop_item = all_stop_ids[all_stop_ids['trip_id']==trip_id]

        start_index = stop_item[stop_item['stop_id']==start_stop_id].index.tolist()[0]

        # get all stops from start stop
        stop_ids.append(stop_item.ix[start_index:]['stop_id'].values)
        stop_times.append(stop_item.ix[start_index:]['arrival_time'].values)

    # for trip_id in trips:
    #     stop_item = all_stop_ids[all_stop_ids['trip_id']==trip_id]
    #     stop_ids.append(stop_item['stop_id'].values)
    #     stop_times.append(stop_item['arrival_time'].values)

    return stop_ids, stop_times


    #
    # all_stop_ids = pd.read_sql("SELECT stop_id,trip_id FROM stop_times WHERE trip_id IN " + "(" + ','.join("{0}".format(x) for x in trips) + ")" , con)
    #
    # stop_ids=[]
    # for trip_id in trips:
    #     stop_id = all_stop_ids[all_stop_ids['trip_id']==trip_id]['stop_id'].values#  pd.read_sql("SELECT stop_id FROM stop_times WHERE trip_id=" + str(trip_id) , con)['stop_id'].values
    #     stop_ids.append(stop_id)
    #
    # # stop_ids = np.unique(stop_ids)
    #
    # return stop_ids




if __name__ == "__main__":
    # lat = 43.7000  # toronto
    # lng = -79.4000
    # lat = 51.135494 # calgary downtown
    # lng = -114.158389

    lat = 51.1699364 # calgary
    lng = -114.12192089999999

    lat = 37.4018732  # san francisco
    lng = -122.1166024

    current_time = datetime.datetime.now()
    #
    ctime = str(current_time.year) + "-" + str(current_time.month) + "-" + str(current_time.day) + "|" + str(current_time.hour) + ":" +str(current_time.minute) + ":" + str(current_time.second)
    ctime = "2016-04-22|09:30:32"
    print(find_accessiable_stops(lat, lng, ctime))

    # cProfile.run('foo() -s time')

    print(find_shape_lat_lng("calgary_ab_canada", 32252846, 3698, 3844))



