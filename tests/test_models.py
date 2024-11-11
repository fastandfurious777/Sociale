from django.test import TestCase
from base.models import Parking


class ParkingTests(TestCase):
    def setUp(self):

        brono_coords = '[(19.880761, 50.082248),(19.884051, 50.082099),(19.883830, 50.080901),(19.880466, 50.081398)]'# Terrain around tram terminal, PKO bang excluded
        Parking.objects.create(name="Notebook", coords = '[(0,0),(1,0),(1,1),(0,1)]')
        Parking.objects.create(name="Bronowice",coords = brono_coords)


    def test_parking(self):
        parking = Parking.objects.get(id=1)
        bronowice = Parking.objects.get(id=2)
        self.assertEqual(parking.name, "Notebook")
        self.assertEqual(parking.coords, "[(0,0),(1,0),(1,1),(0,1)]")
        self.assertEqual(parking.contains_point(0.5,0.5), True)
        self.assertEqual(parking.contains_point(0,0), False)
        self.assertEqual(parking.contains_point(1,1), False)
        self.assertEqual(parking.contains_point(1.01,1.01), False)
        self.assertEqual(parking.contains_point(0.99,0.99), True)

        #Asserting tram terminal is inside polygon/parking
        self.assertEqual(bronowice.contains_point(19.881450,50.081915), True)
        #Asserting PKO terminal is not inside polygon (shouldn't be)
        self.assertEqual(bronowice.contains_point(19.884192, 50.081104), False)
        #To be continued....


