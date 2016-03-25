import csv
import pandas as pd
import numpy as np
import re


def convert_time_string_to_int(time_as_array):
    """
    convert 'hh:mm:ss' time array to int array
    :param time_as_array:
    :return:
    """

    retVal = np.empty_like(time_as_array, dtype=int)
    for i in range(0,len(time_as_array)):
        foo = time_as_array[i].split(":")
        retVal[i] = int(foo[1])*60 + int(foo[2])

        h = int(foo[0])
        if(h>=24): h-=24

        retVal[i] += h*3600

    return retVal


def remove_char_convert_to_int(data_array):

    if(type(data_array[0])!=str):return data_array

    retVal = np.empty_like(data_array, dtype=int)
    for i in range(0, len(data_array)):
        retVal[i] = int(re.sub("[^0-9]+", '', data_array[i]))

    return retVal


# todo parse file name to this function instead of file object
def convert_csv_to_dataframe(csvfile):

    chunksize = 1000

    print('using pandas')

    chunklist=[]
    for chunk in pd.read_csv(csvfile, chunksize=chunksize):
        chunklist.append(_clean_data(chunk))

    data = pd.concat(chunklist, ignore_index=True)

    return data


def save_dataframe_to_db(dataframe, tablename, con):

    sql_query= "DROP TABLE " + tablename
    c = con.cursor()
    c.execute(sql_query)
    con.commit()

    try:
        dataframe.to_sql(tablename, con, if_exists='replace')
    except MemoryError:
        dataframe.to_sql(tablename, con, if_exists='replace', chunksize=1000)


def _clean_data(dataframe):
    must_drop_col = ['shape_dist_traveled']  # todo use must keep list instead ?
    for col_name in dataframe.columns.values.tolist():
        if(col_name in must_drop_col):
            dataframe.drop(col_name, axis=1, inplace=True)

    must_convert_col = ['trip_id', 'route_id', 'stop_id'] # service id?

    for col_name in dataframe.columns.values.tolist():
        if(col_name in must_convert_col):
            dataframe[col_name]=remove_char_convert_to_int(dataframe[col_name])

    must_convert_col = ['arrival_time', 'departure_time']

    for col_name in dataframe.columns.values.tolist():
        if(col_name in must_convert_col):
            dataframe[col_name]=convert_time_string_to_int(dataframe[col_name])

    return dataframe
