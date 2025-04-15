import factory
from random import uniform, randint

from bikes.models import Bike
from users.tests.factories import TestUserFactory


class TestBikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bike

    name = factory.Faker('name')
    lon = factory.LazyFunction(lambda: uniform(0, 3))
    lat = factory.LazyFunction(lambda: uniform(0, 3))
    code = factory.LazyFunction(lambda: randint(1000,9999))
    is_available = factory.Faker('boolean')
    last_taken_by = factory.SubFactory(TestUserFactory)