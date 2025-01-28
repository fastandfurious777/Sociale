from base.models import Bike, Parking, Rental
from base.services import (
    bike_create,
    bike_update,
    bike_delete,
    parking_create,
    parking_update,
    parking_delete,
    rental_create,
    rental_update,
    rental_delete,
    rental_start,
    rental_finish,
    user_create,
    user_update,
    user_delete
    )
from . utils import load_coords

from django.conf import settings
from django.test import TestCase, override_settings
from django.http import Http404
from django.core import exceptions as django_exceptions
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.exceptions import APIException, ValidationError

from datetime import timedelta, datetime
from cryptography import fernet
import warnings

# Suppresses RuntimeWarning: TestResult has no addDuration method bug
warnings.filterwarnings("ignore", category=RuntimeWarning)


class BikeServicesTests(TestCase):
    def setUp(self):
        self.user1: User = User.objects.create_user(**{"username": "John Pork", "email": "johnpork@gmail.com", "password":"Johny123"})
        self.user2: User = User.objects.create_user(**{"username": "Jane Doe", "email": "janedoe@gmail.com", "password": "Jane123"})
        self.bike: Bike = Bike.objects.create(**{"name": "Moongose", "lon": 19.929929, "lat": 50.047412, "code": "9999", "is_available": True})

    def test_bike_create(self):
        """Test a service that creates a bike"""
        bike: Bike = bike_create(name="Marin", lon=19.932672, lat=50.065484, code="1211", is_available=True)
        bike_saved = Bike.objects.get(name="Marin")

        self.assertEqual(bike, bike_saved)
        self.assertIsNotNone(bike_saved.last_updated)
        self.assertTrue(bike_saved.is_available)

        with self.assertRaises(ValidationError):
            bike_create(name="Scott", lon=50.06548, lat=50.065484, code="9919", is_available=False)
        with self.assertRaises(ValidationError):
            bike_create(name="Trek", lon=19.932672, lat=1.940419, code="9999", is_available=True)

    def test_bike_create_encryption(self):
        """Test bike create code encryption"""
        CIPHER_KEY: str = settings.CIPHER_KEY
        bike_code = '9977'
        bike_create(name="Specialized", lon=19.932672, lat=50.065484, code=bike_code, is_available=True)
        encrypted_code: str = Bike.objects.get(name="Specialized").code
        cipher = fernet.Fernet(CIPHER_KEY.encode())
        decrypted_code: str = cipher.decrypt(encrypted_code.encode()).decode()
        self.assertEqual(decrypted_code, bike_code)

    @override_settings(CIPHER_KEY=None)
    def test_bike_create_no_cipher_key(self):
        """Test bike create without a CIPHER_KEY"""
        with self.assertRaises(APIException):
            bike_create(name="Cannondale", lon=19.932672, lat=50.065484, code="7777", is_available=True)

    def test_bike_update(self):
        """Test a service that updates a bike"""
        self.assertNotEqual(self.bike.name, "Updated Bike")
        updated_bike = bike_update(self.bike.id, {"name": "Updated Bike"})
        self.assertEqual(updated_bike.name, "Updated Bike")

        # Ensuring other fields remain unchanged
        self.assertTrue(updated_bike.is_available)
        old_last_updated = updated_bike.last_updated

        updated_bike = bike_update(self.bike.id, {"lon": 19.8, "lat": 50.1, "is_available": False})
        self.assertEqual(updated_bike.lon, 19.8)
        self.assertEqual(updated_bike.lat, 50.1)
        self.assertFalse(updated_bike.is_available)
        self.assertNotEqual(updated_bike.last_updated, old_last_updated)

        # Coordinates outside predefined area, by default Krakow
        with self.assertRaises(ValidationError):
            bike_update(self.bike.id, {"lon": 25.0, "lat": 50.0170})

        with self.assertRaises(ValidationError):
            bike_update(self.bike.id, {"lat": 55.0})
        
        with self.assertRaises(ValidationError):
            bike_update(self.bike.id, {})

        with self.assertRaises(ValidationError):
            bike_update(self.bike.id, {"non_existent_field": "Some Value"})

        with self.assertRaises(ValidationError):
            bike_update(self.bike.id, {"name": "Partial Update", "invalid_field": "Invalid"})

    def test_bike_update_last_taken_by(self):
        updated_bike: Bike = bike_update(self.bike.id, {"last_taken_by": self.user1.id})
        self.assertEqual(updated_bike.last_taken_by, self.user1)

        updated_bike = bike_update(self.bike.id, {"last_taken_by": self.user2.id})
        self.assertEqual(updated_bike.last_taken_by, self.user2)

        with self.assertRaises(Http404):
            bike_update(self.bike.id, {"last_taken_by": 999})

    def test_bike_delete(self):
        """Test a service that deletes a bike"""
        self.assertIn(self.bike, Bike.objects.all())
        bike_delete(self.bike.id)
        self.assertNotIn(self.bike, Bike.objects.all())

        with self.assertRaises(Http404):
            bike_delete(self.bike.id)


class ParkingServicesTests(TestCase):
    def setUp(self):
        self.valid_coords: str = load_coords("inwalidow")
        self.valid_coords2: str = load_coords("ruczaj")
        self.malformed_coords: str = load_coords("malformed")
        self.outside_coords: str = load_coords("sosnowiec")
        self.parking: Parking = Parking.objects.create(**{"name": "Parking", "coords": self.valid_coords})

        
    def test_parking_create(self):
        """Test a service that creates a parking"""
        parking: Parking = parking_create("Inwalidow", self.valid_coords)
        parking_saved: Parking = Parking.objects.get(name="Inwalidow")
        self.assertEqual(parking, parking_saved)
        self.assertEqual(parking_saved.name, "Inwalidow")
        self.assertEqual(parking_saved.coords, self.valid_coords)

        # Ensuring creating a duplicate raises ValidationError
        with self.assertRaises(django_exceptions.ValidationError):
            parking_create("Inwalidow", self.valid_coords)

        with self.assertRaises(ValueError):
            parking_create("Malformed", self.malformed_coords)

        with self.assertRaises(ValidationError):
            parking_create("Empty", '[]')

        with self.assertRaises(ValidationError):
            parking_create("Outside", self.outside_coords)

    def test_parking_update(self):
        """Test a service that updates a parking"""
        updated_parking: Parking = parking_update(self.parking.id,{"name": "New Parking", "coords":self.valid_coords2})
        saved_parking: Parking = Parking.objects.get(name="New Parking")
        self.assertEqual(updated_parking,saved_parking)
        self.assertNotEqual(updated_parking.coords,self.valid_coords)
        self.assertEqual(updated_parking.coords,self.valid_coords2)
        self.assertEqual(updated_parking.name,"New Parking")

        with self.assertRaises(ValidationError):
            parking_update(self.parking.id, {"coords": self.outside_coords})

        with self.assertRaises(ValidationError):
            parking_update(self.parking.id, {"invalid_field": "Invalid"})

        with self.assertRaises(ValidationError):
            parking_update(self.parking.id, {})

    def test_parking_delete(self):
        """Test a service that deletes a parking""" 
        self.assertIn(self.parking, Parking.objects.all())
        parking_delete(self.parking.id)
        self.assertNotIn(self.parking, Parking.objects.all())

        with self.assertRaises(Http404):
            bike_delete(self.parking.id)


class RentalServicesTests(TestCase):
    def setUp(self):
        self.user1: User = User.objects.create_user(**{"username": "John Pork", "email": "johnpork@gmail.com", "password":"Johny123"})
        self.user2: User = User.objects.create_user(**{"username": "Peter Gryffin", "email": "petergryffin@gmail.com", "password":"pg1121"})
        self.bike1: Bike = Bike.objects.create(**{"name": "Scott", "lon": 19.932672, "lat": 50.065484, 'code': '1122', "is_available": True})
        self.bike2: Bike = Bike.objects.create(**{"name": "Marin", "lon": 19.946241, "lat": 50.061592, 'code': '9999', "is_available": True})
        self.bike3: Bike = Bike.objects.create(**{"name": "Moongose", "lon": 19.880761, "lat": 50.082248, 'code': '7171', "is_available": False})
        self.rental: Rental = Rental.objects.create(**{"user": self.user1, "bike": self.bike3,"started_at": timezone.now() })

    def test_rental_create(self):
        """Test a service that creates a rental"""
        start_time: datetime = timezone.now()
        rental: Rental = rental_create(user_id=self.user2.id, bike_id=self.bike2.id,started_at=start_time)
        rental_saved: Rental = Rental.objects.get(user_id=self.user2.id)
        self.assertEqual(rental, rental_saved)
        self.assertEqual(rental.user, self.user2)
        self.assertEqual(rental.bike, self.bike2)
        self.assertIsNotNone(rental.started_at)
        self.assertEqual(rental.started_at, start_time)
        self.assertIsNone(rental.finished_at)

        with self.assertRaises(ValidationError):
            rental_create(user_id=self.user2.id, bike_id=self.bike2.id,started_at=start_time, finished_at=start_time)

    def test_rental_update(self):
        rental_update(id=self.rental.id, data={"user_id": self.user2.id, "bike_id": self.bike2.id})

        self.rental.refresh_from_db()
        self.assertEqual(self.rental.user, self.user2)
        self.assertEqual(self.rental.bike, self.bike2)

        past_time = timezone.now() - timedelta(days=1)

        with self.assertRaises(ValidationError):
            rental_update(id=self.rental.id, data={"finished_at":past_time})
        
        with self.assertRaises(Http404):
            rental_update(id=9999, data={"user_id": self.user1.id})

        with self.assertRaises(ValidationError):
            rental_update(id=self.rental.id, data={"started_at": "invalid-date"})

        with self.assertRaises(ValidationError):
            rental_update(id=self.rental.id, data={})

        with self.assertRaises(ValidationError):
            rental_update(id=self.rental.id, data={"invalid_key":self.user1.id})

    def test_rental_start(self):
        """Test a service that starts a rental"""

        self.assertTrue(self.bike1.is_available)
        self.assertNotEqual(self.bike1.last_taken_by, self.user2.id)
        rental_start(user_id=self.user2.id, bike_id=self.bike1.id)

        self.bike1.refresh_from_db()
        self.assertFalse(self.bike1.is_available)
        self.assertEqual(self.bike1.last_taken_by, self.user2)

        with self.assertRaises(APIException) as context:
            rental_start(user_id=self.user2.id, bike_id=self.bike1.id)
        self.assertIn("Bike is not available", str(context.exception))

        with self.assertRaises(APIException) as context:
            rental_start(user_id=self.user1.id, bike_id=self.bike2.id)
        self.assertIn("Not allowed to start a rental", str(context.exception))
        

    def test_rental_finish(self):
        """Test a service that finishes a rental"""
        parking_create("Inwalidow", load_coords("inwalidow"))

        with self.assertRaises(APIException) as context:
            # Tries to finish ride outside parking
            rental_finish(self.user1.id , 19.880761, 50.082248)
        self.assertIn("Invalid parking location", str(context.exception))

        with self.assertRaises(Http404) as context:
            # Tries to finish ride without starting one
            rental_finish(self.user2.id, 19.925857, 50.069632)

        self.assertFalse(self.bike3.is_available)
        rental_finish(self.user1.id , 19.925857, 50.069632)

        self.bike3.refresh_from_db()
        self.assertTrue(self.bike3.is_available)

        rental: Rental = Rental.objects.get(id=self.rental.id)
        self.assertIsNotNone(rental.finished_at)
    
    def test_rental_delete(self):
        """Test a service that deletes a rental"""
        self.assertIn(self.rental, Rental.objects.all())
        rental_delete(self.rental.id)
        self.assertNotIn(self.rental, Rental.objects.all())

        with self.assertRaises(Http404):
            rental_delete(self.rental.id)


class UserServicesTests(TestCase):
    def setUp(self):
        self.user: User = User.objects.create_user(**{"username": "John Pork", "email": "johnpork@gmail.com", "password":"Johny123"})

    def test_user_create(self):
        """Test a service that creates a user"""
        password: str = "johny123"
        user: User = user_create(username="JohnyM", email="johnym@google.com", password=password)
        user_saved: User = User.objects.get(username="JohnyM")
        self.assertEqual(user, user_saved)
        self.assertNotEqual(password, user_saved.password)

    def test_user_update(self):
        """Test a service that updates a user"""
        updated_data = {"username": "UpdatedPork", "email": "updatedpork@gmail.com"}
        user_update(self.user.id, updated_data)
        updated_user: User = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.username, "UpdatedPork")
        self.assertEqual(updated_user.email, "updatedpork@gmail.com")

        new_password = "NewPork123"
        user_update(self.user.id, {"password": new_password})
        updated_user = User.objects.get(id=self.user.id)
        self.assertNotEqual(new_password, updated_user.password)
        self.assertTrue(updated_user.check_password(new_password))

        with self.assertRaises(ValidationError):
            user_update(self.user.id, {"invalid_field": "value"})

        with self.assertRaises(Http404):
            user_update(999, {"username": "NonExistent"})

    def test_user_delete(self):
        """Test a service that deletes a user"""
        self.assertIn(self.user, User.objects.all())
        user_delete(self.user.id)
        self.assertNotIn(self.user, User.objects.all())

        with self.assertRaises(Http404):
            bike_delete(self.user.id)