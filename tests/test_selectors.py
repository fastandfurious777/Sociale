from django.test import TestCase
from django.http import Http404
from rest_framework.exceptions import APIException
from django.db.models import QuerySet
from django.utils import timezone
from django.contrib.auth.models import User
from base.models import Bike, Parking, Rental
from base.selectors import (
    bike_list,
    bike_get,
    parking_list,
    parking_get,
    rental_list,
    rental_get,
    rental_get_current,
    user_list,
    user_get)
from . utils import load_coords
from datetime import timedelta



class BikeSelectorsTests(TestCase):
    def setUp(self):
        self.bike1: Bike = Bike.objects.create(**{"name": "Scott", "lon": 19.932672, "lat": 50.065484, "is_available": True})
        self.bike2: Bike = Bike.objects.create(**{"name": "Marin", "lon": 19.946241, "lat": 50.061592, "is_available": False})
        self.bike3: Bike = Bike.objects.create(**{"name": "Moongose", "lon": 19.929929, "lat": 50.047412, "is_available": True})

    def test_bike_list(self):
        """Test a selector that lists all available bikes"""
        result: QuerySet[Bike] = bike_list()
        result_names: set[str] =  {bike.name for bike in result}

        self.assertEqual(len(result), 2)
        self.assertSetEqual(result_names, {self.bike1.name,self.bike3.name})
        self.assertNotIn(self.bike2, result)

    def test_bike_get(self):
        """Test a selector that gets bike by id"""
        bike_get_1: Bike = bike_get(self.bike1.id)
        bike_get_2: Bike = bike_get(self.bike2.id)

        self.assertEqual(bike_get_1, self.bike1)
        self.assertTrue(bike_get_1.is_available)
        self.assertFalse(bike_get_2.is_available)
        with self.assertRaises(Http404):
            bike_get(id=100)


class ParkingSelectorsTests(TestCase):
    def setUp(self):
        self.parking1: Parking = Parking.objects.create(**{"name": "Ruczaj", "coords": load_coords("ruczaj")})
        self.parking2: Parking = Parking.objects.create(**{"name": "Bronowice", "coords": load_coords("bronowice")})
        self.parking3: Parking = Parking.objects.create(**{"name": "Inwalidow", "coords": load_coords("inwalidow")})
        
    def test_parking_list(self):
        """Test a selector that lists all parkings"""
        result: QuerySet[Parking] = parking_list()
        result_names: set[str] = {parking.name for parking in result}
        parking_names: set[str] = {self.parking1.name, self.parking2.name, self.parking3.name}

        self.assertEqual(len(result), 3)
        self.assertQuerySetEqual(result, [self.parking1, self.parking2, self.parking3], ordered=False)
        self.assertSetEqual(result_names, parking_names)

        parking_3: Parking = next(parking for parking in result if parking.name == "Inwalidow")
        self.assertEqual(parking_3.coords, load_coords("inwalidow"))
        
    def test_parking_get(self):
        """Test a selector that gets parking by id"""
        parking_get_1: Parking = parking_get(self.parking1.id)
        parking_get_3: Parking = parking_get(self.parking3.id)

        self.assertEqual(parking_get_1, self.parking1)
        self.assertEqual(parking_get_1.name, self.parking1.name)
        self.assertEqual(parking_get_3.coords, self.parking3.coords)
        self.assertNotEqual(parking_get_3.coords, self.parking2.coords)
        with self.assertRaises(Http404):
            parking_get(id=100)


class RentalSelectorsTests(TestCase):
    def setUp(self):
        self.user1: User = User.objects.create_user(**{"username": "John Pork", "email": "johnpork@gmail.com", "password":"Johny123"})
        self.user2: User = User.objects.create_user(**{"username": "Peter Gryffin", "email": "petergryffin@gmail.com", "password":"pg1121"})
        self.user3: User = User.objects.create_user(**{"username": "Quagmire", "email": " giggitygiggity@pronton.com", "password":" giggity"})
        self.bike1: Bike = Bike.objects.create(**{"name": "Scott", "lon": 19.932672, "lat": 50.065484, "is_available": True})
        self.bike2: Bike = Bike.objects.create(**{"name": "Marin", "lon": 19.946241, "lat": 50.061592, "is_available": False})
        self.bike3: Bike = Bike.objects.create(**{"name": "Moongose", "lon": 19.929929, "lat": 50.047412, "is_available": True})
        self.rental1: Rental = Rental.objects.create(**{"user": self.user1, "bike": self.bike1,"started_at": timezone.now(),"finished_at":timezone.now() + timedelta(hours=1) })
        self.rental2: Rental  = Rental.objects.create(**{"user": self.user2, "bike": self.bike2,"started_at": timezone.now(),"finished_at":timezone.now() + timedelta(hours=2) })
        self.rental3: Rental  = Rental.objects.create(**{"user": self.user2, "bike": self.bike2,"started_at": timezone.now()})
        self.rental4: Rental  = Rental.objects.create(**{"user": self.user3, "bike": self.bike2,"started_at": timezone.now()})
        self.rental5: Rental  = Rental.objects.create(**{"user": self.user3, "bike": self.bike3,"started_at": timezone.now()})

    def test_(self):
        """Test a selector that lists all rentals"""
        result: QuerySet[Rental] = rental_list()
        self.assertQuerySetEqual(result, [self.rental1, self.rental2, self.rental3, self.rental4, self.rental5], ordered=False)
        self.assertEqual(len(result), 5)

    def test_rental_get(self):
        """Test a selector that gets rental by id"""
        rental_get_1: Rental = rental_get(self.rental1.id)
        rental_get_2: Rental = rental_get(self.rental2.id)

        self.assertEqual(rental_get_1.user, self.rental1.user)
        self.assertEqual(rental_get_2, self.rental2)
        self.assertNotEqual(rental_get_1.user, self.rental4.user)

    def test_rental_get_current(self):
        """Test a selector that gets current rental for a user"""

        with self.assertRaises(Http404):
            rental_get_current(started_by= self.user1.id)

        with self.assertRaises(APIException):
            # Raises exception if a user has more than one rental active
            rental_get_current(started_by=self.user3.id)

        rental_get_unfinished: Rental = rental_get_current(started_by=self.user2.id)
        self.assertEqual(rental_get_unfinished, self.rental3)


class UserSelectorsTests(TestCase):
    def setUp(self):
        self.user1: User = User.objects.create_user(**{"username": "John Pork", "email": "johnpork@gmail.com", "password":"Johny123"})
        self.user2: User = User.objects.create_user(**{"username": "Peter Gryffin", "email": "petergryffin@gmail.com", "password":"pg1121"})
        self.user3: User = User.objects.create_user(**{"username": "Quagmire", "email": " giggitygiggity@pronton.com", "password":" giggity"})

    def test_user_list(self):
        """Test a selector that lists all users"""
        result: QuerySet[User] = user_list()

        self.assertEqual(len(result), 3)
        usernames = [user.username for user in result]
        self.assertIn("John Pork", usernames)
        self.assertIn("Peter Gryffin", usernames)
        self.assertIn("Quagmire", usernames)

    def test_user_get(self):
        """Test a selector that gets user by id"""
        user_get_1 = user_get(self.user1.id)
        self.assertIsNotNone(user_get_1)
        self.assertEqual(user_get_1.username, "John Pork")
        self.assertNotEqual(user_get_1.password, "Johny123")