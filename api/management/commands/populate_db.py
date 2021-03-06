"""
This script is used to load gtfs data into database
To populate database, from project root folder:
>>> python manage.py populate_db

"""

from datetime import datetime

import pandas as pd
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from api.models import Stop, Calender, Route, Shape, Trip, StopTime
from api.repo import insert_route, insert_service, insert_shape, insert_stop, insert_stop_time, insert_trip


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    gtfs = 'api/management/commands/gtfs/'

    def _get_file(self, file_name):
        """
        Get gtfs file to laod
        :param file_name:
        :return:
        """
        return self.gtfs + file_name

    def _parse_date(self, date):
        """
        Convert date string to date for saving in django
        :param date:
        :return:
        """
        return datetime.strptime(date, "%Y%m%d").date()

    def _parse_time(self, t):
        """
        Parse time, there are scenarios where hour is 24 or 25, which throws error, this handles it
        :param t:
        :return:
        """
        ts = t.split(":")
        d = int(ts[0])
        f = d % 24
        t = "{}:{}:{}".format(f, ts[1], ts[2])

        return datetime.strptime(t, '%H:%M:%S').time()

    @atomic
    def _load_stop(self):
        print("Loading stops")
        df = pd.read_csv(self._get_file('stops.txt'))

        Stop.objects.all().delete()
        for index, row in df.iterrows():
            insert_stop(row['stop_id'], row['stop_name'], row['stop_lat'], row['stop_lon'])

    @atomic
    def _load_calender(self):
        print("Loading calendar")
        df = pd.read_csv(self._get_file('calendar.txt'), dtype=str)

        Calender.objects.all().delete()
        for index, row in df.iterrows():
            insert_service(service_id=row['service_id'],
                           monday=row['monday'],
                           tuesday=row['tuesday'],
                           wednesday=row['wednesday'],
                           thursday=row['thursday'],
                           friday=row['friday'],
                           saturday=row['saturday'],
                           sunday=row['sunday'],
                           start_date=self._parse_date(row['start_date']),
                           end_date=self._parse_date(row['end_date']))

    @atomic
    def _load_route(self):
        print("Loading routes")
        df = pd.read_csv(self._get_file('routes.txt'), dtype=str)

        Route.objects.all().delete()
        for index, row in df.iterrows():
            insert_route(route_id=row['route_id'],
                         route_long_name=row['route_long_name'],
                         route_short_name=row['route_short_name'])

    @atomic
    def _load_shape(self):
        print("Loading shapes")
        df = pd.read_csv(self._get_file('shapes.txt'), dtype=str)

        Shape.objects.all().delete()
        for index, row in df.iterrows():
            insert_shape(shape_id=row['shape_id'],
                         shape_pt_lat=row['shape_pt_lat'],
                         shape_pt_lon=row['shape_pt_lon'],
                         shape_pt_sequence=row['shape_pt_sequence'])

    @atomic
    def _load_trip(self):
        print("Loading trips")
        df = pd.read_csv(self._get_file('trips.txt'), dtype=str)

        Trip.objects.all().delete()
        for index, row in df.iterrows():
            insert_trip(trip_id=row['trip_id'],
                        route_id=row['route_id'],
                        service_id=row['service_id'],
                        shape_id=row['shape_id'])

    @atomic
    def _load_stop_time(self):
        print("Loading stop_times")
        df = pd.read_csv(self._get_file('stop_times.txt'), dtype=str)

        StopTime.objects.all().delete()
        for index, row in df.iterrows():
            insert_stop_time(trip_id=row['trip_id'],
                             arrival_time=row['arrival_time'],
                             departure_time=row['departure_time'],
                             stop_id=row['stop_id'],
                             stop_sequence=row['stop_sequence'])

    def handle(self, *args, **options):
        self._load_stop()
        self._load_calender()
        self._load_route()
        self._load_shape()
        self._load_trip()
        self._load_stop_time()
