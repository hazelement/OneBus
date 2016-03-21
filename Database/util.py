
import numpy as np



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

