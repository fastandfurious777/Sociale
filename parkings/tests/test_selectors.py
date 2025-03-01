from django.test import TestCase
from parkings.models import Parking
from parkings.selectors import (
    parking_list, 
    parking_list_active,
    parking_get,
    parking_get_by_name,
    check_parking_location
)
from django.http import Http404

class TestParkingSelectors(TestCase):

    @classmethod
    def setUpTestData(cls):

        active_parking_area = {
            "type": "Polygon", 
            "coordinates": [[[0, 0], [0, 4], [4, 4], [4, 0], [0, 0]]]}
        inactive_parking_area = {
            "type": "Polygon",
            "coordinates": [[[5, 5], [10, 10], [0, 10], [5, 5]]]
        }
        cls.active_parking = Parking.objects.create(
            name="ActiveParking", area=active_parking_area, is_active=True
        ) 
        cls.inactive_parking = Parking.objects.create(
            name="InactiveParking", area=inactive_parking_area, is_active=False
        ) 

    def test_parking_list(self):
        parkings = parking_list()
        self.assertEqual(parkings.count(), 2)

    def test_parking_list_active(self):
        parkings = parking_list_active()
        self.assertEqual(parkings.count(), 1)
        self.assertEqual(parkings[0].name, "ActiveParking")

    def test_parking_get(self):
        parking = parking_get(2)
        self.assertEqual(parking, self.inactive_parking)

    def test_parking_get_nonexistent(self):
        with self.assertRaises(Http404):
            parking_get(999) 

    def test_parking_get_by_name(self):
        parking = parking_get_by_name("ActiveParking")
        self.assertEqual(parking, self.active_parking)

    def test_parking_get_by_name_nonexistent(self):
        with self.assertRaises(Http404):
            parking_get_by_name("ActiveParkin")

    def check_parking_location_valid(self):
        self.assertTrue(check_parking_location(1, 1))

    def check_parking_location_invalid(self):
        point = (5, 6)

        # Ensuring that check_parking_location only considers active parkings
        self.assertTrue(self.inactive_parking.contains_point(*point))
        self.assertFalse(check_parking_location(*point))