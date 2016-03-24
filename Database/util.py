import csv
import pandas as pd
import numpy as np
import re


def convert_time_string_to_int(time_as_array):
    '''
    convert 'hh:mm:ss' time array to int array
    :param time_as_array:
    :return:
    '''

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


def convert_csv_file_to_pd(csvfile):
    try:
        print('using pandas')
        data = pd.read_csv(csvfile,engine='c')
    except:
        print('pandas failed, using alternative')
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)

        data = pd.DataFrame(columns=header)

        i=0
        for row in reader:
            data.loc[i]=row
            i+=1

    must_drop_col = ['shape_dist_traveled']  # use must keep list instead ?
    for col_name in data.columns.values.tolist():
        if(col_name in must_drop_col):
            data.drop(col_name, axis=1, inplace=True)

    must_convert_col = ['trip_id', 'route_id', 'stop_id'] # service id?

    for col_name in data.columns.values.tolist():
        if(col_name in must_convert_col):
            data[col_name]=remove_char_convert_to_int(data[col_name])

    must_convert_col = ['arrival_time', 'departure_time']

    for col_name in data.columns.values.tolist():
        if(col_name in must_convert_col):
            data[col_name]=convert_time_string_to_int(data[col_name])


    return data