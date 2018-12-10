# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models


# todo add POI interest and save search locations to this database

# Create your models here.
@python_2_unicode_compatible
class Stop(models.Model):
    stop_id = models.CharField(primary_key=True, max_length=255)
    stop_name = models.CharField(max_length=255)
    stop_lat = models.FloatField()
    stop_lon = models.FloatField()

    def __str__(self):
        return "stop_id: {}, stop_name: {}".format(self.stop_id, self.stop_name)


@python_2_unicode_compatible
class Calender(models.Model):
    service_id = models.CharField(primary_key=True, max_length=255)
    monday = models.IntegerField()
    tuesday = models.IntegerField()
    wednesday = models.IntegerField()
    thursday = models.IntegerField()
    friday = models.IntegerField()
    saturday = models.IntegerField()
    sunday = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return "service_id: {}, start_date: {}, end_date: {}".format(self.service_id, self.start_date, self.end_date)


@python_2_unicode_compatible
class Route(models.Model):
    route_id = models.CharField(primary_key=True, max_length=255)
    route_short_name = models.CharField(max_length=255, default="")
    route_long_name = models.CharField(max_length=255)

    def __str__(self):
        return "route_id: {}, route_long_name: {}".format(self.route_id, self.route_long_name)


@python_2_unicode_compatible
class Shape(models.Model):
    class Meta:
        unique_together = ('shape_id', 'shape_pt_sequence',)

    shape_id = models.CharField(primary_key=True, max_length=255)
    shape_pt_lat = models.FloatField()
    shape_pt_lon = models.FloatField()
    shape_pt_sequence = models.IntegerField()

    def __str__(self):
        return "shape_id: {}, shape_pt_lat: {}, shape_pt_lon: {}, shape_pt_sequence: {}".format(
            self.shape_id, self.shape_pt_lat, self.shape_pt_lon, self.shape_pt_sequence)


@python_2_unicode_compatible
class Trip(models.Model):
    trip_id = models.CharField(primary_key=True, max_length=255)
    route_id = models.ForeignKey(Route, db_column='route_id')
    service_id = models.ForeignKey(Calender, db_column='service_id')
    shape_id = models.ForeignKey(Shape, db_column='shape_id')

    def __str__(self):
        return "trip_id: {}, route_id: {}, service_id: {}".format(self.trip_id, self.route_id, self.service_id)


@python_2_unicode_compatible
class StopTime(models.Model):
    class Meta:
        unique_together = ('trip_id', 'stop_id', 'stop_sequence')

    trip_id = models.ForeignKey(Trip, db_column='trip_id')
    arrival_time = models.IntegerField()  # in seconds, can't use datetime because operating hours go beyond 24 hours
    departure_time = models.IntegerField()  # in seconds
    stop_id = models.ForeignKey(Stop, db_column='stop_id')
    stop_sequence = models.IntegerField()

    def __str__(self):
        return "trip_id: {}, arrival_time: {}, departure_time: {}".format(
            self.trip_id, self.arrival_time, self.departure_time)

    def to_latlon_matrix(self):
        return {"trip_id": self.trip_id.trip_id,
                "route_id": self.trip_id.route_id.route_id,
                "stop_id": self.stop_id.stop_id,
                "stop_lat": self.stop_id.stop_lat,
                "stop_lon": self.stop_id.stop_lon,
                "time": self.arrival_time,
                "stop_sequence": self.stop_sequence
                }
