from django.test import TestCase
from base.models import Bike, Parking
from base.selectors import (
    bike_list,
    bike_get,
    parking_list,
    parking_get,
    rental_list,
    rental_get)
from django.http import Http404
from .coords import DB



# Create your tests here.

class BikeSelectorsTests(TestCase):
    def setUp(self):
        Bike.objects.create(name="Scott", lon=19.932672, lat = 50.065484, is_available=True)
        Bike.objects.create(name="Marin", lon=19.946241, lat = 50.061592, is_available=False)
        Bike.objects.create(name="Moongose", lon=19.929929, lat = 50.047412, is_available=True)

    def test_bike_list(self):
        """Test a selector that lists all available bikes"""
        result = bike_list()
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "Scott")
        self.assertEqual(result[1].name, "Moongose")

    def test_bike_get(self):
        """Test a selector that gets bike by id"""
        bike1 = bike_get(id=1)
        bike2 = bike_get(id=2)

        self.assertEqual(bike1.name, "Scott")
        self.assertEqual(bike1.is_available, True)
        self.assertEqual(bike2.name, "Marin")
        self.assertEqual(bike2.is_available, False)
        with self.assertRaises(Http404):
            bike_get(id=4)

class ParkingSelectorsTests(TestCase):
    def setUp(self):
        Parking.objects.create(name="Ruczaj", coords=DB['ruczaj'])
        Parking.objects.create(name="Bronowice", coords=DB['bronowice'])
        Parking.objects.create(name="Inwalidow", coords=DB['inwalidow'])


    def test_parking_list(self):
        """Test a selector that lists all parkings"""
        result = parking_list()
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].name, "Ruczaj")
        self.assertEqual(result[0].coords, '[(19.906198, 50.018914),(19.911552, 50.018065), (19.909752, 50.016239), (19.903646, 50.017568)]')
        self.assertEqual(result[2].name, "Inwalidow")


    def test_parking_get(self):
        """Test a selector that gets parking by id"""
        with self.assertRaises(Http404):
            parking_get(id=4)

class RentalSelectorsTests(TestCase):
    def setUp(self):
        pass

    def test_rental_list(self):
        """Test a selector that lists all rentals based on their status"""
        #result = parking_list()
        
        #self.assertEqual(len(result), 3)


    def test_rental_get(self):
        """Test a selector that gets rental by id"""
        pass

