from django.test import TestCase
from django.http import Http404

from bikes.models import Bike
from bikes.services import bike_create, bike_update, bike_delete
from bikes.tests.factories import TestBikeFactory
from users.tests.factories import TestUserFactory
from parkings.tests.factories import TestParkingFactory


class BikeTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.parking = TestParkingFactory.create()
        cls.bike = TestBikeFactory.create(is_available=True)

    def test_bike_create(self):
        bike_create(name="Bike", lon=1, lat=1, code=1215, is_available=True)
        bike = Bike.objects.filter(name="Bike").first()
        self.assertEqual(bike.code, 1215)

    def test_bike_update(self):
        user = TestUserFactory.create()
        update_data = {
            "name": "BikeUpdated",
            "lon": 2,
            "lat": 2,
            "code": 67890,
            "is_available": False,
            "last_taken_by": user.id,
        }

        bike_update(self.bike.id, data=update_data)
        self.bike.refresh_from_db()
        self.assertEqual(self.bike.name, "BikeUpdated")

    def test_bike_update_nonexistent(self):
        with self.assertRaises(Http404):
            bike_update(999, {"name": "Scott"})

    def test_bike_delete(self):
        bike_delete(self.bike.id)
        self.assertFalse(Bike.objects.filter(id=self.bike.id).exists())
        with self.assertRaises(Http404):
            bike_delete(self.bike.id)
