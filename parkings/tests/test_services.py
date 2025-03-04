
from django.test import TestCase
from parkings.models import Parking
from parkings.services import parking_create, parking_update, parking_delete
from django.http import Http404
from rest_framework.exceptions import ValidationError


class ParkingServicesTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.parking_area = {
            "type": "Polygon", 
            "coordinates": [[[0, 0], [0, 4], [4, 4], [4, 0], [0, 0]]]
        }

        cls.outside_area = {
            "type": "Polygon", 
            "coordinates": [[[0, 0], [0, 11], [11, 11], [4, 0], [0, 0]]]
        }

        boundary_area = {
            "type": "Polygon", 
            "coordinates": [[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]]
        }

        cls.boundary = Parking.objects.create(
            name="boundary", area=boundary_area
        ) 
        cls.parking = Parking.objects.create(
            name="Parking", area=cls.parking_area, is_active=False
        ) 

    def test_parking_create(self):
        new_area = {
            "type": "Polygon", 
            "coordinates": [[[0, 0], [0, 3], [3, 3], [0, 0]]]
        }

        parking_create(
            name="NewParking",
            capacity=12,
            area=new_area
        )
        created_parking = Parking.objects.get(name="NewParking")
        self.assertEqual(created_parking.area, new_area)
        self.assertTrue(created_parking.is_active)

    def test_parking_create_outside_boundaries(self):
        with self.assertRaises(ValidationError) as cm:
            parking_create(
                name="InvalidParking",
                capacity=10,
                area=self.outside_area  
            )
        self.assertEqual(cm.exception.detail["detail"], "Parking area cannot exceed outer boundaries")

    def test_parking_create_invalid_capacity(self):
        with self.assertRaises(ValidationError):
            parking_create(name="InvalidParking", capacity=-5, area=self.parking_area)
    
    def test_parking_update(self):
        self.assertFalse(self.parking.is_active)
        data = {
        "area": {
            "type": "Polygon", 
            "coordinates": [[[0, 0], [0, 3], [3, 3], [0, 0]]]
        },
        "is_active": True
        }
        parking_update(self.parking.id, data)
        
        self.parking.refresh_from_db()
        
        self.assertTrue(self.parking.is_active)
        self.assertEqual(self.parking.area, data["area"])
   
    def test_parking_update_invalid(self):
        with self.assertRaises(ValidationError) as cm:
            parking_update(self.parking.id, {"area": self.outside_area})
        self.assertEqual(cm.exception.detail["detail"], "Parking area cannot exceed outer boundaries")

        with self.assertRaises(ValidationError)as cm:
            parking_update(self.parking.id, {"invalid_field": "value"})
        self.assertEqual(cm.exception.detail["detail"], "Field 'invalid_field' is not meant to be updated")

        with self.assertRaises(Http404):
            parking_update(999, {"name": "Nonexistent parking"})

    def test_parking_delete(self):
        self.assertIn(self.parking, Parking.objects.all())
        parking_delete(self.parking.id)
        self.assertNotIn(self.parking, Parking.objects.all())
        with self.assertRaises(Http404):
            parking_delete(self.parking.id)    