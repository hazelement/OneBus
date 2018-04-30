# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models


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
    route_long_name = models.CharField(max_length=255)

    def __str__(self):
        return "route_id: {}, route_long_name: {}".format(self.route_id, self.route_long_name)


@python_2_unicode_compatible
class Shape(models.Model):
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
    trip_headsign = models.CharField(max_length=255)

    def __str__(self):
        return "trip_id: {}, route_id: {}, service_id: {}".format(self.trip_id, self.route_id, self.service_id)


@python_2_unicode_compatible
class StopTime(models.Model):
    trip_id = models.ForeignKey(Trip, db_column='trip_id')
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    stop_id = models.ForeignKey(Stop, db_column='stop_id')
    stop_sequence = models.IntegerField()

    def __str__(self):
        return "trip_id: {}, arrival_time: {}, departure_time: {}".format(
            self.trip_id, self.arrival_time, self.departure_time)