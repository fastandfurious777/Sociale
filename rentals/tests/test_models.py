from rest_framework.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from rentals.models import Rental
from users.tests.factories import TestUserFactory
from bikes.tests.factories import TestBikeFactory

class RentalTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = TestUserFactory.create()
        cls.bike = TestBikeFactory.create()

    def test_clean_valid_dates(self):
        rental = Rental(
            user=self.user,
            bike=self.bike,
            started_at=timezone.now(),
            finished_at=timezone.now() + timezone.timedelta(hours=1),
            status=Rental.Status.STARTED
        )
        try:
            rental.clean()  
        except ValidationError:
            self.fail("Validation Error was raised incorrectly")

    def test_clean_invalid_dates(self):
        rental = Rental(
            user=self.user,
            bike=self.bike,
            started_at=timezone.now(),
            finished_at=timezone.now() - timezone.timedelta(hours=1),
            status=Rental.Status.STARTED
        )
        with self.assertRaises(ValidationError) as cm:
            rental.clean()
        self.assertIn("Rental finish date cannot be before the start date", str(cm.exception))

    def test_clean_multiple_started_rentals(self):
        rental_before = Rental(
            user=self.user,
            bike=TestBikeFactory.create(),
            started_at=timezone.now(),
            status=Rental.Status.STARTED
        )
        rental_before.save()

        rental = Rental(
            user=self.user,
            bike=self.bike,
            started_at=timezone.now(),
            status=Rental.Status.STARTED
        )
        with self.assertRaises(ValidationError) as cm:
            rental.clean()
        self.assertIn("You cannot have more than one rental started", str(cm.exception))

    def test_clean_single_started_rental(self):
        rental = Rental(
            user=self.user,
            bike=self.bike,
            started_at=timezone.now(),
            status=Rental.Status.STARTED
        )
        try:
            rental.clean()
        except ValidationError:
            self.fail("Validation Error was raised incorrectly")