from django.test import TestCase
from django.http import Http404
from users.selectors import user_list, user_get, user_get_by_email
from users.tests.factories import TestUserFactory


class TestUserSelectors(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = TestUserFactory.create(email="test@example.com")
        TestUserFactory.create(email="email@sociale.com")

    def test_user_list(self):
        users = user_list()
        self.assertEqual(users.count(), 2)

    def test_user_get_existing_user(self):
        retrieved_user = user_get(self.user.id)

        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.id, self.user.id)

    def test_user_get_nonexistent_user(self):
        with self.assertRaises(Http404):
            user_get(9999)

    def test_user_get_by_email_existing_user(self):
        retrieved_user = user_get_by_email("test@example.com")
        self.assertEqual(retrieved_user.email, "test@example.com")

    def test_user_get_by_email_nonexistent_user(self):
        with self.assertRaises(Http404):
            user_get_by_email("nonexistent@example.com")
