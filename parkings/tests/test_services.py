import json
from django.test import TestCase
from django.http import Http404
from rest_framework.exceptions import ValidationError
from parkings.tests.factories import TestParkingFactory
from parkings.models import Parking
from parkings.services import parking_create, parking_update, parking_delete


class ParkingServicesTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.outside_area = {
            "type": "Polygon",
            "coordinates": [[[0, 0], [0, 11], [11, 11], [4, 0], [0, 0]]],
        }
        cls.valid_area = {
            "type": "Polygon",
            "coordinates": [[[0, 0], [0, 3], [3, 3], [0, 0]]],
        }

        cls.boundary = TestParkingFactory.create(
            name="boundary", coords=[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]
        )
        cls.parking = TestParkingFactory.create(
            name="Parking",
            coords=[[0, 0], [0, 4], [4, 4], [4, 0], [0, 0]],
            is_active=False,
        )

    def test_parking_create(self):
        parking_create(name="NewParking", capacity=12, area=json.dumps(self.valid_area))
        created_parking = Parking.objects.get(name="NewParking")
        self.assertEqual(json.loads(created_parking.area), self.valid_area)
        self.assertTrue(created_parking.is_active)

    def test_parking_create_outside_boundaries(self):

        with self.assertRaises(ValidationError) as cm:
            parking_create(
                name="InvalidParking", capacity=10, area=json.dumps(self.outside_area)
            )

        self.assertIn("Parking area cannot exceed outer boundary", str(cm.exception))

    def test_parking_create_invalid_capacity(self):
        with self.assertRaises(ValidationError):
            parking_create(
                name="InvalidParking", capacity=-5, area=json.dumps(self.valid_area)
            )

    def test_parking_update(self):
        self.assertFalse(self.parking.is_active)
        data = {
            "area": json.dumps(self.valid_area),
            "is_active": True,
        }
        parking_update(self.parking.id, data)

        self.parking.refresh_from_db()

        self.assertTrue(self.parking.is_active)
        self.assertEqual(self.parking.area, data["area"])

    def test_parking_update_invalid(self):
        with self.assertRaises(ValidationError) as cm:
            parking_update(self.parking.id, {"area": json.dumps(self.outside_area)})

        self.assertIn("Parking area cannot exceed outer boundary", str(cm.exception))

        with self.assertRaises(ValidationError) as cm:
            parking_update(self.parking.id, {"invalid_field": "value"})
        self.assertIn(
            "Field 'invalid_field' is not meant to be updated", str(cm.exception)
        )

    def test_parking_update_nonexistent(self):
        with self.assertRaises(Http404):
            parking_update(999, {"name": "Nonexistent parking"})

    def test_parking_delete(self):
        self.assertIn(self.parking, Parking.objects.all())
        parking_delete(self.parking.id)
        self.assertNotIn(self.parking, Parking.objects.all())
        with self.assertRaises(Http404):
            parking_delete(self.parking.id)
