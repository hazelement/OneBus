
from math import cos, pi
from datetime import datetime, timedelta
import pandas as pd

from models import Route, Calender, Shape, Trip, StopTime, Stop

DAYOFWEEK_MAPPING = {0: 'monday',
                     1: 'tuesday',
                     2: 'wednesday',
                     3: 'thursday',
                     4: 'friday',
                     5: 'saturday',
                     6: 'sunday'}

# todo implement delete method and replace populate_db.py with this method

def parse_date(date):
    """
    Convert date string to date for saving in django
    :param date: date string in "%Y%m%d"
    :return:
    """
    return datetime.strptime(date, "%Y%m%d").date()


def insert_service(service_id, start_date, end_date, monday, tuesday, wednesday, thursday, friday, saturday, sunday):
    """
    Insert a new service
    :param service_id: str, service_id
    :param start_date: date object, start date of service
    :param end_date: date object, end date of service
    :param active_week_days: list of active work days,
                ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    :return:
    """
    calender = Calender(service_id=service_id,
                        monday=monday,
                        tuesday=tuesday,
                        wednesday=wednesday,
                        thursday=thursday,
                        friday=friday,
                        saturday=saturday,
                        sunday=sunday,
                        start_date=parse_date(start_date),
                        end_date=parse_date(end_date))
    calender.save()


def insert_route(route_id, route_short_name, route_long_name):
    """
    insert a new route
    :param route_id: str, route id
    :param route_short_name: str, short name for route
    :param route_long_name: str, long name for route
    :return:
    """
    d = Route(route_id=route_id,
              route_short_name=route_short_name,
              route_long_name=route_long_name)
    d.save()


def insert_shape(shape_id, shape_pt_lat, shape_pt_lon, shape_pt_sequence):
    """
    insert a new shape record
    :param shape_id: str, shape id
    :param shape_pt_lat: float, latitude of shape point
    :param shape_pt_lon: float, longitude of shape point
    :param shape_pt_sequence: int, sequence of shape point
    :return:
    """
    d = Shape(shape_id=shape_id,
              shape_pt_lat=shape_pt_lat,
              shape_pt_lon=shape_pt_lon,
              shape_pt_sequence=shape_pt_sequence)
    d.save()


def insert_trip(trip_id, route_id, service_id, shape_id):
    """
    insert a new trip
    :param trip_id: str, id of trip
    :param route_id: str, id of route
    :param service_id: str, id of service,
    :param shape_id: str, id of shape
    :return:
    """
    route = Route.objects.get(route_id=route_id)
    service = Calender.objects.get(service_id=service_id)

    d = Trip(trip_id=trip_id,
             route_id=route,
             service_id=service,
             shape_id=shape_id)
    d.save()


def insert_stop(stop_id, stop_name, stop_lat, stop_lon):
    """
    insert a new stop
    :param stop_id: str, stop id
    :param stop_name: str, name of stop
    :param stop_lat: float, latitude
    :param stop_lon: float, longitude
    :return:
    """
    d = Stop(stop_id=stop_id,
             stop_name=stop_name,
             stop_lat=stop_lat,
             stop_lon=stop_lon)
    d.save()


def insert_stop_time(stop_id, trip_id, arrival_time, departure_time, stop_sequence):
    """

    :param stop_id: str, id of stop
    :param trip_id: str, id of trip
    :param arrival_time: time, arrival time
    :param departure_time: time, departure time
    :param stop_sequence: int, sequence of the stop in the trip
    :return:
    """
    stop = Stop.objects.get(stop_id=stop_id)
    trip = Stop.objects.get(trip_id=trip_id)

    d = StopTime(stop_id=stop,
                 trip_id=trip,
                 arrival_time=parse_date(arrival_time),
                 departure_time=parse_date(departure_time),
                 stop_sequence=stop_sequence)
    d.save()


def meter_to_lat_lon(lat, lon, displacement):
    """
    Convert displacement in meters to changes in lat and lon
    :param lat: float, latitude at which displacement occurred
    :param lon: float, longitude at which displacement occurred
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

    dayofweek = DAYOFWEEK_MAPPING[date.weekday()]

    kwargs = {"start_date__lte": date,
              "end_date__gte": date,
              dayofweek: 1}

    return Calender.objects.filter(**kwargs).all()


def get_start_stop(trip, potential_start_stops):
    """
    Get stop that a trip given a list of stop to start from
    :param trip: Trip objects
    :param potential_start_stops: Stop object
    :return:
    """

    start_stop = StopTime.objects.filter(trip_id=trip, stop_id__in=potential_start_stops).first()

    return start_stop


def get_following_stops(stops, services, current_time, time_scope=1):
    """
    Get a list of stops following given stops and service id
    :param stops: list of Stop object, nearby stops
    :param services: list of Calender object, available services
    :param current_time: datetime object, current time
    :param time_scope: int, how many hours to look into in the future for trips
    :return: pandas dataframe containing trip_id, route_id, stop_id, stop_lat, stop_lon, time, stop_sequence as columns
    """

    # trips that are accessible from these stops
    stop_trips = StopTime.objects.filter(stop_id__in=stops,
                                         arrival_time__gte=current_time.time(),
                                         arrival_time__lte=(current_time + timedelta(hours=time_scope)).time(),
                                         trip_id__service_id__in=services).all()

    # find stop times along these trips
    accessible_stops = []
    for stop_trip in stop_trips:
        temp = StopTime.objects.filter(trip_id=stop_trip.trip_id,
                                       stop_sequence__gte=stop_trip.stop_sequence).all()
        accessible_stops.extend(temp)

    # convert to pandas dataframe for later matrix calculation
    df = pd.DataFrame([stop_time.to_latlon_matrix() for stop_time in accessible_stops])\
        .drop_duplicates(subset=['trip_id', 'stop_id', 'time'])

    return df