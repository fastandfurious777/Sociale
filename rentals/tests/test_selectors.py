from rest_framework.exceptions import APIException
from django.test import TestCase
from django.http import Http404

from rentals.models import Rental
from rentals.selectors import rental_list, rental_get, rental_get_current_by_user
from rentals.tests.factories import TestRentalFactory
from users.tests.factories import TestUserFactory
from bikes.tests.factories import TestBikeFactory


class TestRentalSelectors(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = TestUserFactory.create()
        cls.user2 = TestUserFactory.create()

        cls.bike1 = TestBikeFactory.create()
        cls.bike2 = TestBikeFactory.create()

        cls.rental1 = TestRentalFactory.create(
            user=cls.user1, bike=cls.bike1, status=Rental.Status.STARTED
        )
        cls.rental2 = TestRentalFactory.create(
            user=cls.user1, bike=cls.bike2, status=Rental.Status.FINISHED
        )
        cls.rental3 = TestRentalFactory.create(
            user=cls.user2, bike=cls.bike2, status=Rental.Status.STARTED
        )

    def test_rental_list(self):
        rentals = rental_list({"user_id": self.user1.id, "status": "started"})
        self.assertEqual(rentals.count(), 1)
        self.assertIn(self.rental1, rentals)

    def test_rental_list_no_status(self):
        rentals = rental_list({"user_id": self.user1.id})
        self.assertEqual(rentals.count(), 2)

    def test_rental_list_no_user(self):
        rentals = rental_list({"status": "finished"})
        self.assertEqual(rentals.count(), 1)

    def test_rental_get(self):
        rental = rental_get(self.rental2.id)
        self.assertEqual(rental, self.rental2)

    def test_rental_get_nonexistent(self):
        with self.assertRaises(Http404):
            rental_get(999)

    def test_rental_get_current_by_user(self):
        rental = rental_get_current_by_user(self.user1.id)
        self.assertEqual(rental, self.rental1)

    def test_rental_get_current_by_user_multiple_active(self):
        TestRentalFactory.create(user=self.user1, status=Rental.Status.STARTED)
        with self.assertRaises(APIException):
            rental_get_current_by_user(self.user1.id)
