import factory
from users.models import User

class TestUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    password = factory.django.Password('pw')
    is_active = True
