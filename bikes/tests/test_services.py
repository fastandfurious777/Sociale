from django.test import TestCase
from parkings.models import Parking
from bikes.models import Bike
from users.models import User
from bikes.services import bike_create, bike_update, bike_delete
from django.http import Http404


class BikeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        boundary_area = {
            "type": "Polygon",
            "coordinates": [[[0, 0], [0, 3], [3, 3], [3, 0], [0, 0]]]
        }
        cls.boundary = Parking.objects.create(name="boundary", area=boundary_area)

        cls.bike = Bike.objects.create(
            name="AvailableBike",
            lon=1, lat=1,
            code=67890,
            is_available=True,
        )
    
    def test_bike_create(self):
        bike = bike_create(
            name="Bike",
            lon=1, lat=1,
            code=1215,
            is_available=True
        )
        bike = Bike.objects.filter(name="Bike").first()
        self.assertEqual(bike.code, 1215)
    
    def test_bike_update(self):
        user = User.objects.create(
            email="123@gmail.com"
        )
        update_data = dict(
            name="BikeUpdated",
            lon=2, lat=2,
            code=67890,
            is_available=False,
            last_taken_by=user.id
        )
        bike_update(
            self.bike.id,
            data=update_data
        )
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