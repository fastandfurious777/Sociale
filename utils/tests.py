from rest_framework.test import APITestCase, APIClient
from django.core.cache import cache
from users.models import User


class CustomAPITestCase(APITestCase):

    @classmethod
    def setUpAuthData(cls):
        cls.client = APIClient()
        cls.admin = User.objects.create_superuser(
            email="admin@sociale.com", password="admin"
        )

        cls.active_user = User.objects.create_user(
            email="chillguy@sociale.com",
            password="ilovesociale",
            is_active=True,
            is_verified=True,
        )
        
        cls.verified_not_active_user = User.objects.create_user(
            email="user@noverify.com",
            password="noverify",
            is_active=False,
            is_verified=True,
        )

    def tearDown(self):
        cache.clear()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)
