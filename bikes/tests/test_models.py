from django.test import TestCase
from parkings.models import Parking
from rest_framework.exceptions import ValidationError
from bikes.models import Bike
from users.models import User
class BikeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        boundary_area = {
            "type": "Polygon",
            "coordinates": [[[0, 0], [0, 3], [3, 3], [3, 0], [0, 0]]]
        }
        cls.boundary = Parking.objects.create(name="boundary", area=boundary_area)
        

    def test_last_taken_by_user(self):
        user = User.objects.create(email="testuser")
        bike = Bike(
            name="Bike",
            lon=1, lat=1,
            code=67890,
            is_available=False,
            last_taken_by=user
        )
        self.assertEqual(bike.last_taken_by, user)

    def test_qr_code_generation(self):
        bike = Bike(
            name="Bike",
            lon=1, lat=1,
            code=11111,
            is_available=True
        )
        self.assertIsNotNone(bike.qr_code)

    def test_coords_outside_boundaries(self):
        bike = Bike(
            name="Bike",
            lon=4, lat=1,
            code=11111,
            is_available=True
        )
        with self.assertRaises(ValidationError) as ctx:
            bike.full_clean()
        
        detail = ctx.exception.detail['detail']
        self.assertEqual(detail, "Bike cannot be parked outside boundary")