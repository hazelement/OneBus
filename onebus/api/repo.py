
from datetime import datetime

from models import Route, Calender, Shape, Trip, StopTime, Stop
WEEKDAY = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


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



def get_service_id(request_date):
    """
    get service id given a date
    :param request_date: python date object
    :return: Calender object
    """
    week_day = request_date.weekday()  # Monday is 0 and Sunday is 6



    kwargs = {
        WEEKDAY[week_day]: 1,
        'start_date__level__lte': request_date,
        'end_date__level__gte': request_date
    }

    service = Calender.objects.filter(**kwargs)