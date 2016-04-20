
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


class GtfsRawDataParser():

    _service_id_mapping = {}
    _trip_id_mapping = {}
    _route_id_mapping = {}

    _city_code = ""
    _zipfile = "zipfile"

    con = "sqlite connection"

    def __init__(self, city_code):
        self._city_code = city_code

        current_folder = os.path.dirname(os.path.realpath(__file__)) + "/"
        db_name = current_folder + "SQLData/" +self._city_code + ".sqlite"

        self.con = sqlite3.connect(db_name)

        self._service_id_mapping = {}
        self._trip_id_mapping = {}
        self._route_id_mapping = {}

    def fetch_new_data(self):

        self._download_zip()

        self._process_agency()
        self._process_calendar()
        self._process_calendar_dates()
        self._process_routes()
        self._process_trips()
        self._process_stops()
        self._process_stop_times()
        self._process_shapes()

        return

    def _download_zip(self):
        print("updating database for " + self._city_code)
        print("downloading from transitfeed.com " + self._city_code)

        request = requests.get(config.read_city_url_from_config(self._city_code))
        self._zipfile = ZipFile(BytesIO(request.content))
        print("download finished")

    def _process_agency(self):
        fname = 'agency'
        print("processing " + fname)

        data = self._convert_csv_to_dataframe(self._zipfile.open(fname + ".txt"))

        self._save_dataframe_to_db(data, fname)

    def _process_shapes(self):
        fname = 'shapes'
        print("processing " + fname)

        data = self._convert_csv_to_dataframe(self._zipfile.open(fname + ".txt"))

        self._save_dataframe_to_db(data, fname)

    def _process_stops(self):
        fname = 'stops'
        print("processing " + fname)

        data = self._convert_csv_to_dataframe(self._zipfile.open(fname + ".txt"))

        self._save_dataframe_to_db(data, fname)

    def _process_stop_times(self):
        fname = 'stop_times'
        print("processing " + fname)

        data = self._convert_csv_to_dataframe(self._zipfile.open(fname + ".txt"))

        must_convert_col = ['arrival_time', 'departure_time']  # convert time in string to integer
        for col_name in data.columns.values.tolist():
            if(col_name in must_convert_col):
                data[col_name]=util.convert_time_string_to_int(data[col_name])

        self._save_dataframe_to_db(data, fname)

    def _process_calendar(self):
        fname = 'calendar'
        print("processing " + fname)

        data = self._convert_csv_to_dataframe(self._zipfile.open(fname + ".txt"))

        self._save_dataframe_to_db(data, fname)

    def _process_calendar_dates(self):
        fname = 'calendar_dates'
        print("processing " + fname)

        data = self._convert_csv_to_dataframe(self._zipfile.open(fname + ".txt"))

        self._save_dataframe_to_db(data, fname)

    def _process_trips(self):
        fname = 'trips'
        print("processing " + fname)

        data = self._convert_csv_to_dataframe(self._zipfile.open(fname + ".txt"))

        self._save_dataframe_to_db(data, fname)

    def _process_routes(self):
        fname = 'routes'
        print("processing " + fname)

        data = self._convert_csv_to_dataframe(self._zipfile.open(fname + ".txt"))

        self._save_dataframe_to_db(data, fname)


    def _mapping_pre_check(self, data, column_name):
        if(column_name not in data.columns.values):
            return True

        if(type(data[column_name].values[0]) != str):
            return True

        return False

    def _remapping(self, data):

        data = self._remap_service_id(data)
        data = self._remap_route_id(data)
        data = self._remap_trip_id(data)
        return  data

    def _remap_service_id(self, data):

        if(self._mapping_pre_check(data, 'service_id')): return data

        if(self._service_id_mapping == {}):  # if mapping is not created, create now
            service_ids = np.unique(data['service_id'].values)

            count = 0
            for service_id in service_ids:
                self._service_id_mapping[service_id] = count
                count+=1

        data.replace({'service_id': self._service_id_mapping}, inplace=True)
        data[['service_id']]=data[['service_id']].astype(int)

        return data

    def _remap_trip_id(self, data):

        if(self._mapping_pre_check(data, 'trip_id')): return data


        if(self._trip_id_mapping == {}):  # if mapping is not created, create now
            trip_ids = np.unique(data['trip_id'].values)

            count = 0
            for trip_id in trip_ids:
                self._trip_id_mapping[trip_id] = count
                count+=1

        data.replace({'trip_id': self._trip_id_mapping}, inplace=True)
        data[['trip_id']]=data[['trip_id']].astype(int)

        return data

    def _remap_route_id(self, data):

        if(self._mapping_pre_check(data, 'route_id')): return data

        if(self._route_id_mapping == {}):  # if mapping is not created, create now
            route_ids = np.unique(data['route_id'].values)

            count = 0
            for route_id in route_ids:
                self._route_id_mapping[route_id] = route_id.split('-')[0]
                count+=1

        data.replace({'route_id': self._route_id_mapping}, inplace=True)
        data[['route_id']]=data[['route_id']].astype(int)

        return data

    def _convert_csv_to_dataframe(self, csvfile):

        chunksize = 1000

        print('using pandas')

        chunklist=[]
        for chunk in pd.read_csv(csvfile, chunksize=chunksize):
            chunklist.append(chunk)

        data = pd.concat(chunklist, ignore_index=True)

        print('perform remapping')

        data = self._remapping(data)

        return data

    def _save_dataframe_to_db(self, dataframe, tablename):

        try:
            dataframe.to_sql(tablename, self.con, if_exists='replace')
        except MemoryError:
            dataframe.to_sql(tablename, self.con, if_exists='replace', chunksize=1000)

#todo different city seems to have different data format, maybe keep useful ones only and line up data value and types

def update_all_database():
    config = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/city_url.config')

    city_codes = config['city'].values

    for city in city_codes:
        try:
            print "Garbage collection: ", gc.collect()
            print "unreachable garbage: ", gc.collect()
            ds = GtfsRawDataParser('city')
            ds.fetch_new_data()
        except Exception,e:
            print(e)
            pass

if __name__ == "__main__":

    # ds = DataBaseParser('calgary_ab_canada')
    # ds.fetch_new_data()
    update_all_database()
    # list = ["23:42:23", "32:01:32"]
    # _update_city_database('calgary_ab_canada')
    # _update_city_database('toronto_on_canada')
    # _update_city_database('edmonton_ab_canada')
    # _update_city_database('vancouver_bc_canada')
    # _update_city_database('sanfranciso_ca_us')

    #
    # print(convert_time_string_to_int(list))


