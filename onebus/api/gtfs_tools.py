from math import cos, pi
from datetime import datetime, timedelta
from models import Calender, Stop, StopTime, Trip

dayofweek_mapping = {0: 'monday',
                     1: 'tuesday',
                     2: 'wednesday',
                     3: 'thursday',
                     4: 'friday',
                     5: 'saturday',
                     6: 'sunday'}


def meter_to_lat_lon(lat, lon, displacement):
    """
    Convert displacement in meters to changes in lat and lon
    :param lat: float, latitude
    :param lon: float, longitude
    :param displacement: float, displacement in meters
    :return: angular displacement in latitude degree, angular displacement in longitude
    """
    lat = lat/180 * pi
    lon = lon/180 * pi
    lat_displacement = 1.0/111111 * displacement
    lon_displacement = 1.0/(111111 * cos(lat)) * displacement
    return lat_displacement, lon_displacement


def get_nearby_stops(lat, lon, radius=200):
    """
    Find bus stop around location given
    :param lat: float, latitude
    :param lon: float, longigude
    :param radius: float, radius (meter) to look for
    :return:
    """

    lat_rad, lon_rad = meter_to_lat_lon(lat, lon, radius)

    kwargs = { "stop_lat__lte": lat + lat_rad,
               "stop_lat__gte": lat - lat_rad,
               "stop_lon__lte": lon + lon_rad,
               "stop_lon__gte": lon - lon_rad
    }

    return Stop.objects.filter(**kwargs).all()


def get_available_services(date):
    """
    Get service_id by date
    :param date: date object
    :return: list of calender objects
    """

    dayofweek = dayofweek_mapping[date.weekday()]

    kwargs = {"start_date__lte": date,
              "end_date__gte": date,
              dayofweek: 1}

    return Calender.objects.filter(**kwargs).all()


def get_nearby_trips(stops, services, current_time, time_scope=1):
    """

    :param stops: list of Stop object, nearby stops
    :param services: list of Calender object, available services
    :param current_time: datetime object, current time
    :param time_scope: int, how many hours to look into in the future for trips
    :return: list of StopTime object which contains trips, time and stop id
    """

    trips = StopTime.objects.filter(stop_id__in=stops,
                                    arrival_time__gte=current_time.time(),
                                    arrival_time__lte=(current_time + timedelta(hours=time_scope)).time(),
                                    trip_id__service_id__in=services).all()

    print(trips)


