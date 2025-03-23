from django.test import TestCase
from unittest.mock import patch
from rest_framework.exceptions import ValidationError
from bikes.models import Bike
from bikes.tests.factories import TestBikeFactory
from users.tests.factories import TestUserFactory


class BikeTests(TestCase):

    def test_qr_code_generation(self):
        bike = Bike(name="Bike", lon=1, lat=1, code=11111, is_available=True)
        self.assertIsNotNone(bike.qr_code)

    @patch("bikes.models.check_parking_location", return_value=True)
    def test_start_rent(self, mocked_check):
        user = TestUserFactory()
        bike = TestBikeFactory(is_available=True)
        bike.start_rent(user)

        self.assertFalse(bike.is_available)
        self.assertEqual(bike.last_taken_by, user)

    @patch("bikes.models.check_parking_location", return_value=True)
    def test_start_rent_bike_unavailable(self, mocked_check):
        user = TestUserFactory()
        bike = TestBikeFactory(is_available=False)

        with self.assertRaises(ValidationError) as cm:
            bike.start_rent(user)
        self.assertIn("Bike is not available", str(cm.exception))

    @patch("bikes.models.check_parking_location", return_value=True)
    def test_finish_rent(self, mocked_check):
        bike = TestBikeFactory(is_available=False)
        # Assuming there is a valid parking at 1.0, 1.0
        new_lon = 1.0
        new_lat = 1.0
        bike.finish_rent(new_lon, new_lat)

        self.assertTrue(bike.is_available)
        self.assertEqual(bike.lon, new_lon)
        self.assertEqual(bike.lat, new_lat)

    @patch("bikes.models.check_parking_location", return_value=False)
    def test_finish_rent_invalid_location(self, mocked_check):
        bike = TestBikeFactory(is_available=False)
        with self.assertRaises(ValidationError) as cm:
            bike.finish_rent(4.0, 1.0)
        self.assertIn("Bike is not in a parking location", str(cm.exception))
