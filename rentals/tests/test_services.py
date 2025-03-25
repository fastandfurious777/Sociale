from rest_framework.exceptions import APIException
from django.test import TestCase

from rentals.models import Rental
from rentals.services import rental_start, rental_finish, rental_update, rental_delete
from rentals.selectors import rental_get_current_by_user
from rentals.tests.factories import TestRentalFactory
from users.tests.factories import TestUserFactory
from bikes.tests.factories import TestBikeFactory
from parkings.tests.factories import TestParkingFactory


class TestRentalSelectors(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = TestUserFactory.create()
        cls.bike1 = TestBikeFactory.create(is_available=True)
        cls.bike2 = TestBikeFactory.create(is_available=True)

        TestParkingFactory.create(
            name="boundary", coords=[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]
        )

    def test_rental_start(self):
        rental_start(user_id=self.user.id, bike_id=self.bike1.id)

    def test_rental_start_with_started_rental(self):
        TestRentalFactory.create(user=self.user, status=Rental.Status.STARTED)
        with self.assertRaises(APIException) as cm:
            rental_start(user_id=self.user.id, bike_id=self.bike2.id)
        self.assertIn("You cannot have more than one rental started", str(cm.exception))

    def test_rental_start_rented_bike(self):
        rental_start(user_id=self.user.id, bike_id=self.bike1.id)
        TestRentalFactory.create(bike=self.bike1, status=Rental.Status.STARTED)
        with self.assertRaises(APIException) as cm:
            diffrent_user = TestUserFactory.create()
            rental_start(user_id=diffrent_user.id, bike_id=self.bike1.id)
        self.assertIn("Bike is not available", str(cm.exception))

    def test_rental_finish(self):
        rental_start(user_id=self.user.id, bike_id=self.bike1.id)
        rental = rental_get_current_by_user(user_id=self.user.id)
        rental_finish(user_id=self.user.id, lon=2, lat=2)

        rental.refresh_from_db()
        self.assertEqual(rental.status, Rental.Status.FINISHED)

    def test_rental_finish_not_in_parking_area(self):
        rental_start(user_id=self.user.id, bike_id=self.bike1.id)
        with self.assertRaises(APIException) as cm:
            rental_finish(user_id=self.user.id, lon=11, lat=11)
        self.assertIn("Bike is not in a parking location", str(cm.exception))

    def test_rental_update(self):
        rental = TestRentalFactory.create(status=Rental.Status.STARTED)
        new_status = "finished"
        rental_update(rental_id=rental.id, data={"status": new_status})
        rental.refresh_from_db()
        self.assertEqual(rental.status, Rental.Status.FINISHED.value)

    def test_rental_delete(self):
        rental = TestRentalFactory.create()
        rental_delete(rental_id=rental.id)
        with self.assertRaises(Rental.DoesNotExist):
            Rental.objects.get(id=rental.id)
