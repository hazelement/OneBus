
import pandas as pd
import numpy as np
import re
import config


def result_filter_by_distance(stops, targets):
    """
    return filtered index of stops, and targets
    :param stops: array of stops to reference from
    :param targets: array of targets to filter through
    :return:
    """

    # generate distance matrix
    distance_matrix = distance_calc(stops, targets)

    min_target_distance = np.amin(distance_matrix, axis=0)

    if(len(targets) > 20):
        threshold = 0.010
    else:
        threshold = 0.020

    # find targets are closest to stops
    target_mapping = min_target_distance<threshold

    # find stops that are closest to these targets
    stop_mapping = np.argmin(distance_matrix, axis=0)

    return stop_mapping[target_mapping], target_mapping  # selecting only stops that are closed to good targets


def ramerdouglas(line, dist):
    """Does Ramer-Douglas-Peucker simplification of
    a line with `dist` threshold.
    `line` must be a list of Vec objects,
    all of the same type (either 2d or 3d)."""
    if len(line) < 3:
        return line

    begin, end = line[0], line[-1]
    distSq = [begin.distSq(curr) -
        ((end - begin) * (curr - begin)) ** 2 /
        begin.distSq(end) for curr in line[1:-1]]

    maxdist = max(distSq)
    if maxdist < dist ** 2:
        return [begin, end]

    pos = distSq.index(maxdist)
    return (ramerdouglas(line[:pos + 2], dist) +
            ramerdouglas(line[pos + 1:], dist)[1:])

def distance_calc(array1, array2):
    """
    calculate distance between two arrays of coordinates, return
    :param array1:
    :param array2:
    :return: mxn matrix
    """
    # a^2 - 2ab + b^2
    dot_p = np.dot(array1, np.transpose(array2))

    item2 = -2.0 * dot_p

    array1 = np.square(array1)
    array2 = np.square(array2)

    sum1= np.sum(array1, axis = 1)
    sum2 = np.sum(array2, axis = 1)

    item1 = np.repeat(np.transpose([sum1]), len(sum2), axis = 1)
    item3 = np.repeat([sum2], len(sum1), axis = 0)

    retVal = item1 + item2 + item3

    return np.sqrt(retVal)

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



def convert_csv_to_dataframe(csvfile, city_code):

    chunksize = 1000

    print('using pandas')

    chunklist=[]
    for chunk in pd.read_csv(csvfile, chunksize=chunksize):
        chunklist.append(_clean_data(chunk, city_code))

    data = pd.concat(chunklist, ignore_index=True)

    return data


def save_dataframe_to_db(dataframe, tablename, con):

    try:
        dataframe.to_sql(tablename, con, if_exists='replace')
    except MemoryError:
        dataframe.to_sql(tablename, con, if_exists='replace', chunksize=1000)


def _clean_data(dataframe, city_code):
    must_drop_col = ['shape_dist_traveled']  # todo use must keep column header list instead ?
    for col_name in dataframe.columns.values.tolist():
        if(col_name in must_drop_col):
            dataframe.drop(col_name, axis=1, inplace=True)

    must_convert_col = ['trip_id', 'stop_id'] # service id?

    for col_name in dataframe.columns.values.tolist():
        if(col_name in must_convert_col):
            dataframe[col_name]=_remove_char_convert_to_int(dataframe[col_name])

    must_convert_col = ['route_id']
    for col_name in dataframe.columns.values.tolist():
        if(col_name in must_convert_col):
            dataframe[col_name]=_process_route_id(dataframe[col_name], city_code)


    must_convert_col = ['arrival_time', 'departure_time']

    for col_name in dataframe.columns.values.tolist():
        if(col_name in must_convert_col):
            dataframe[col_name]=convert_time_string_to_int(dataframe[col_name])

    return dataframe

def _process_route_id(data_array, city_code):
    if(type(data_array[0])!=str):return data_array

    try:
        retVal = np.empty_like(data_array, dtype=int)
        for i in range(0, len(data_array)):
            # retVal[i] = int(data_array[i].split(config.read_route_id_process_key(city_code))[0])
            retVal[i] = data_array[i].split(config.read_route_id_process_key(city_code))[0]
    except ValueError:
        pass

    return retVal

def _remove_char_convert_to_int(data_array):

    if(type(data_array[0])!=str):return data_array

    retVal = np.empty_like(data_array, dtype=int)
    for i in range(0, len(data_array)):
        retVal[i] = int(re.sub("[^0-9]+", '', data_array[i].split('-')[0]))

    return retVal