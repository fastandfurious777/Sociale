from django.test import TestCase
from base.models import Parking
from rest_framework.exceptions import ValidationError

from .coords import DB

class ParkingTests(TestCase):
    def setUp(self):

        brono_coords = DB['bronowice']# Terrain around tram terminal, pko bank excluded
        chocimska_coords = DB['chocimska']
        Parking.objects.create(name="Notebook", coords = '[(0,0),(1,0),(1,1),(0,1)]')
        Parking.objects.create(name="Bronowice",coords = brono_coords)
        Parking.objects.create(name="Chocimska",coords = chocimska_coords)


    def test_parking_contains_point(self):
        """Tests if method 'contains_point' works properly"""
        parking = Parking.objects.get(id=1)
        bronowice = Parking.objects.get(id=2)
        chocimska = Parking.objects.get(id=3)
        self.assertEqual(parking.contains_point(0.5,0.5), True)
        self.assertEqual(parking.contains_point(0,0), False)
        self.assertEqual(parking.contains_point(1,1), False)
        self.assertEqual(parking.contains_point(1.01,1.01), False)
        self.assertEqual(parking.contains_point(0.99,0.99), True)
        self.assertEqual(bronowice.contains_point(19.881450, 50.081915), True)
        self.assertEqual(bronowice.contains_point(19.884192, 50.081104), False)
        self.assertEqual(chocimska.contains_point(19.916172, 50.068739), True)
        self.assertEqual(chocimska.contains_point(19.920293, 50.068289), False)
    
    def test_parking_clean(self):
        """Tests if using 'full_clean' method on 'Parking' object works fine"""
        with self.assertRaises(ValidationError):
            sosnowiec_coords = DB['sosnowiec']
            sosnowiec = Parking(name='Sosnowiec',coords=sosnowiec_coords)
            sosnowiec.full_clean()








