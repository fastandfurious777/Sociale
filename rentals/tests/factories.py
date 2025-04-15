import factory
from django.utils import timezone
from datetime import timedelta

from rentals.models import Rental
from users.tests.factories import TestUserFactory
from bikes.tests.factories import TestBikeFactory


class TestRentalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rental

    bike = factory.SubFactory(TestBikeFactory)
    user = factory.SubFactory(TestUserFactory)

    # LazyFunction requires a callable; using timezone.now() directly (as linters suggest) won't work
    started_at = factory.LazyFunction(lambda: timezone.now())
    finished_at = factory.LazyFunction(lambda: timezone.now() + timedelta(days=1))
    status = factory.Faker('random_element', elements=['started', 'finished', 'canceled'])