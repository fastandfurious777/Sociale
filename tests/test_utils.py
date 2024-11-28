from django.test import TestCase
from datetime import datetime
from base.utils import date_validate, parking_location_validate
from rest_framework.exceptions import ValidationError
from .coords import DB
from base.models import Parking

class DateValidateTests(TestCase):

    def test_date_validate(self):
        valid_date = datetime(2024,11,11,22,21,00)
        diffrent_date = datetime(2024,11,12,22,21,00)
        valid_date_str = '2024-11-11 22:21:00'
        invalid_date_str = '22-11-11 22:21:00'
        invalid_int = 41

        self.assertIsInstance(date_validate(valid_date_str), datetime)
        self.assertEqual(date_validate(valid_date_str), valid_date)
        self.assertEqual(date_validate(valid_date), valid_date)
        self.assertNotEqual(date_validate(valid_date_str), diffrent_date)

        with self.assertRaises(ValidationError):
            date_validate(invalid_date_str)

        with self.assertRaises(ValidationError):
            date_validate(invalid_int) # type: ignore

class ParkingValidateTests(TestCase):

    def setUp(self):
        Parking.objects.create(name="Ruczaj", coords=DB['ruczaj'])
        Parking.objects.create(name="Bronowice", coords=DB['bronowice'])
        Parking.objects.create(name="Inwalidow", coords=DB['inwalidow'])

    def test_parking_validate(self):
        parkings = Parking.objects.all()
        self.assertTrue(parking_location_validate(19.881450, 50.081915, parkings))
        self.assertFalse(parking_location_validate(19.884192, 50.081104, parkings))

        
