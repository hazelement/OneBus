# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, RequestFactory

from .views import query


class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/query?lat=51.173569&lon=-114.118553&datetime=2018-04-29_18:47:05')

        # Test my_view() as if it were deployed at /customer/details
        response = query(request)
        self.assertEqual(response.status_code, 200)