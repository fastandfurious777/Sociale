import json
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from parkings.models import Parking
from parkings.tests.factories import TestParkingFactory


class ParkingTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.parking = TestParkingFactory.create()
        cls.boundary = TestParkingFactory(
            name="boundary", coords=[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]
        )

    def test_parking_contains_point(self):
        self.assertTrue(self.parking.contains_point(1, 1))
        self.assertFalse(self.parking.contains_point(6, 5))

    def test_parking_inside_boundary(self):
        self.parking.full_clean()

    def test_parking_outside_boundary(self):
        outside_area = {
            "type": "Polygon",
            "coordinates": [[[0, 0], [0, 11], [10, 11], [10, 0], [0, 0]]],
        }
        outside_parking = Parking(name="OutsidePark", area=json.dumps(outside_area))

        with self.assertRaises(ValidationError):
            outside_parking.full_clean()

    def test_geojson_missing_coordinates(self):
        invalid_area = {"type": "Polygon"}

        invalid_parking = Parking(name="InvalidParking", area=json.dumps(invalid_area))

        with self.assertRaises(ValidationError) as cm:
            invalid_parking.get_polygon_from_area()

        self.assertIn("Parking area is invalid", str(cm.exception))

    def test_geojson_invalid_type(self):
        invalid_area = {
            "type": "Point",
            "coordinates": [[[0, 0], [1, 1], [1, 0], [0, 0]]],
        }
        invalid_parking = Parking(name="InvalidParking", area=json.dumps(invalid_area))

        with self.assertRaises(ValidationError) as cm:
            invalid_parking.get_polygon_from_area()

        self.assertIn("Parking area is invalid", str(cm.exception))
