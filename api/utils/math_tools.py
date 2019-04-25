
import pandas as pd
import numpy as np
import re
import config
from math import sin, cos, sqrt, atan2, radians


def result_filter_by_distance(stops, targets):
    """
    return filtered index of stops, and targets
    :param stops: array of stops to reference from
    :param targets: array of targets to filter through
    :return: stop mapping and poi mapping, these are POI that are close to stops and their corresponding stops
    """
    # import pdb;pdb.set_trace()
    # generate distance matrix
    distance_matrix = distance_calc(stops, targets)

    min_target_distance = np.amin(distance_matrix, axis=0)

    threshold = 0.01


    # if(len(targets) > 20):
    #     threshold = 0.008
    # else:
    #     threshold = 0.016

    # find targets are closest to stops
    target_mapping = min_target_distance<threshold

    # find stops that are closest to these targets
    stop_mapping = np.argmin(distance_matrix, axis=0)

    # select stops that matches selected target
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
    calculate distance between two arrays of coordinates, return a matrix containing distance between coordinates in
    each array
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

def measure(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance * 1000
