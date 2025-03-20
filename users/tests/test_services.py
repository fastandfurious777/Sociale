from django.test import TestCase
from django.http import Http404
from rest_framework.exceptions import ValidationError
from users.models import User
from users.services import user_create, user_update, user_delete
from users.tests.factories import TestUserFactory


class UserServicesTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = TestUserFactory.create()

    def test_user_create(self):
        password = "johny123"
        user = user_create(
            email="johnym@google.com",
            password=password,
            first_name="Johny",
            last_name="Bugaj",
        )

        user.refresh_from_db()
        self.assertNotEqual(password, user.password)
        self.assertEqual(user.email, "johnym@google.com")

    def test_user_update(self):
        updated_data = {"email": "updatedpork@gmail.com"}
        user_update(self.user.id, updated_data)
        self.user.refresh_from_db()

        self.assertEqual(self.user.email, "updatedpork@gmail.com")

    def test_user_update_invalid(self):
        with self.assertRaises(ValidationError):
            user_update(self.user.id, {"username": "Invalid"})

    def test_user_update_nonexistent(self):
        with self.assertRaises(Http404):
            user_update(999, {"username": "NonExistent"})

    def test_user_delete(self):
        self.assertIn(self.user, User.objects.all())
        user_delete(self.user.id)
        self.assertNotIn(self.user, User.objects.all())
        
        with self.assertRaises(Http404):
            user_delete(self.user.id)
