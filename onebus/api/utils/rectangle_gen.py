import numpy as np


class Point(object):
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng


class Rectangle(object):
    def __init__(self, p1, p2):
        self.p_sw = self._update_p_sw(p1, p2)
        self.p_ne = self._update_p_ne(p1, p2)

    def _update_p_sw(self, p1, p2):
        return Point(min(p1.lat, p2.lat), min(p1.lng, p2.lng))

    def _update_p_ne(self, p1, p2):
        return Point(max(p1.lat, p2.lat), max(p1.lng, p2.lng))

    def update_rec(self, p):
        self.p_sw = self._update_p_sw(self.p_sw, p)
        self.p_ne = self._update_p_ne(self.p_ne, p)

    def calc_area(self):
        lat_side = abs(self.p_sw.lat - self.p_ne.lat)
        lng_side = abs(self.p_sw.lng - self.p_ne.lng)

        return lat_side * lng_side


def get_search_rectangles(stop_gps):
    """
    Generate a list of rectanges based on a list of
    :param stop_gps: numpy array of stop gps,  [[lat, lon], [lat, lon]]
    :return: numpy array of rectanges
    """

    # size of rectangle
    lat_delta = 0.02
    lng_delta = 0.02

    # get sw and ne corner among all the stops
    p_sw = Point(min(stop_gps[:, 0]) - lat_delta, min(stop_gps[:, 1]) - lng_delta)
    p_ne = Point(max(stop_gps[:, 0]) + lat_delta, max(stop_gps[:, 1]) + lng_delta)

    # get big rectangle
    parent_rec = Rectangle(p_sw, p_ne)

    # generate small rectangles from sw to ne
    lat_array = np.arange(parent_rec.p_sw.lat, parent_rec.p_ne.lat, lat_delta)
    lng_array = np.arange(parent_rec.p_sw.lng, parent_rec.p_ne.lng, lng_delta)

    rec_list = []

    for i in range(0, len(lat_array) - 1):
        rec_list.append([lat_array[i], lng_array[i], lat_array[i + 1], lng_array[i + 1]])

    rec_list = np.array(rec_list)
    return rec_list
