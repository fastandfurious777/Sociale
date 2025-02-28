from django.test import TestCase
from parkings.models import Parking
from rest_framework.exceptions import ValidationError
class ParkingTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        parking_area = {
            "type": "Polygon", 
            "coordinates": [[[0, 0], [0, 4], [4, 4], [4, 0], [0, 0]]]}
        boundary_area = {
            "type": "Polygon",
            "coordinates": [[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]]
        }
        cls.parking = Parking(name="TestPark", area=parking_area) 
        cls.boundary = Parking.objects.create(name="boundary", area=boundary_area)
        cls.boundary.save()

    def test_parking_contains_point(self):
        self.assertTrue(self.parking.contains_point(1, 1))
        self.assertFalse(self.parking.contains_point(6, 5))

    def test_parking_inside_boundary(self):
        try:
            self.parking.full_clean()  
        except ValidationError:
            self.fail("Validation Error was raised incorrectly")

    def test_parking_outside_boundary(self):
        outside_area = {
        "type": "Polygon",
        "coordinates": [[[0, 0], [0, 11], [10, 11], [10, 0], [0, 0]]]
        }
        outside_parking = Parking(name="OutsidePark", area=outside_area)
        
        with self.assertRaises(ValidationError):
            outside_parking.full_clean()

    def test_geojson_missing_coordinates(self):
        invalid_area = {"type": "Polygon"}
        
        invalid_parking = Parking(name="InvalidParking", area=invalid_area)
        
        with self.assertRaises(ValidationError) as cm:
            invalid_parking.get_polygon_from_area()

        self.assertEqual(cm.exception.detail["detail"], "GeoJSON must contain 'type' and 'coordinates' fields")
        
    def test_geojson_invalid_type(self):
        invalid_area = {"type": "Point", "coordinates": [[[0, 0], [1, 1], [1, 0], [0, 0]]]}
        
        invalid_parking = Parking(name="InvalidParking", area=invalid_area)
        
        with self.assertRaises(ValidationError) as cm:
            invalid_parking.get_polygon_from_area()

        self.assertEqual(cm.exception.detail["detail"], "Invalid type. Expected 'Polygon', but received 'Point'")

    def test_geojson_invalid_coordinates_(self):
        invalid_area = {"type": "Polygon", "coordinates": [[0, 0], [1, 1], [1, 0], [0, 0]]}
        
        invalid_parking = Parking(name="InvalidParking", area=invalid_area)
        
        with self.assertRaises(ValidationError) as cm:
            invalid_parking.get_polygon_from_area()

        self.assertEqual(cm.exception.detail["detail"], "Polygon must have at least 4 coordinate pairs")