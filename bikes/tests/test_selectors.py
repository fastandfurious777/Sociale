from django.test import TestCase
from bikes.models import Bike
from bikes.selectors import bike_get, bike_list
from django.http import Http404


class BikeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.bike_available = Bike.objects.create(
            name="BikeAv",
            lon=1, lat=1,
            code=67890,
            is_available=True,
        )
        cls.bike_unavailable = Bike.objects.create(
            name="BikeUn",
            lon=2, lat=2,
            code=1111,
            is_available=False,
        )
        
    def test_bike_list(self):
        bikes = bike_list()
        self.assertEqual(bikes.count(), 1)
        self.assertEqual(bikes[0].name, "BikeAv")

    def test_bike_list_all(self):
        bikes = bike_list(include_unavailable=True)
        self.assertEqual(bikes.count(), 2)

    def test_bike_get(self):
        bike = bike_get(self.bike_unavailable.id)
        self.assertEqual(bike, self.bike_unavailable)

    def test_bike_get_nonexistent(self):
        with self.assertRaises(Http404):
            bike_get(999)