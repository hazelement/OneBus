# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, RequestFactory

from repo import insert_stop_time, insert_trip, insert_shape, insert_route, insert_service, insert_stop

# from .views import query
#
#
# class SimpleTest(TestCase):
#     def setUp(self):
#         # Every test needs access to the request factory.
#         self.factory = RequestFactory()
#
#     def test_details(self):
#         # Create an instance of a GET request.
#         request = self.factory.get('/query?lat=51.173569&lon=-114.118553&datetime=2018-04-29_18:47:05')
#
#         # Test my_view() as if it were deployed at /customer/details
#         response = query(request)
#         self.assertEqual(response.status_code, 200)

class DBSetupTest(TestCase):

    trip_id = "t1"
    service_id = "s1"
    route_id = "r1"
    shape_id = "shape1"
    stop_id = "stop1"

    def setUp(self):
        insert_service(self.service_id, '20180910', '20180912', 1, 0, 1, 0, 1, 1, 1)
        insert_route(self.route_id, "short route", "long route")

        insert_shape(self.shape_id, "31.213", "-124.2312", 1)
        insert_shape(self.shape_id, "31.213", "-124.234", 2)

        insert_trip(self.trip_id, self.route_id, self.service_id, self.shape_id)
        insert_stop(self.stop_id, "test stop", "31.313", "-124.244")

        insert_stop_time(self.stop_id, self.trip_id, "14:23", "14:24", 1)

    def test_exaple(self):
        """Animals that can speak are correctly identified"""
        pass

# todo write test for repo.py