from uuid import uuid4
from django.test import TestCase
from django.http import Http404
from bikes.tests.factories import TestBikeFactory
from bikes.selectors import bike_get, bike_list, bike_get_by_qrcode


class BikeTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.bike_available = TestBikeFactory.create(is_available=True)
        cls.bike_unavailable = TestBikeFactory.create(is_available=False)

    def test_bike_list(self):
        bikes = bike_list()
        self.assertEqual(bikes.count(), 1)
        self.assertEqual(bikes[0], self.bike_available)

    def test_bike_list_all(self):
        bikes = bike_list(include_unavailable=True)
        self.assertEqual(bikes.count(), 2)

    def test_bike_get(self):
        bike = bike_get(self.bike_unavailable.id)
        self.assertEqual(bike, self.bike_unavailable)

    def test_bike_get_nonexistent(self):
        with self.assertRaises(Http404):
            bike_get(999)

    def test_bike_get_by_qr(self):
        bike = bike_get_by_qrcode(self.bike_available.qr_code)
        self.assertEqual(bike, self.bike_available)

    def test_bike_get_qr_nonexistent(self):
        with self.assertRaises(Http404):
            bike_get_by_qrcode(uuid4())
