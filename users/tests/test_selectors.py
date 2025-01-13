from django.test import TestCase
from users.selectors import user_list, user_get, user_get_by_email
from .factories import TestUserFactory 
 

class TestUserSelectors(TestCase):

    def test_user_list(self):
        TestUserFactory.create_batch(3)
        users = user_list()
        self.assertEqual(users.count(), 3)

    def test_user_get_existing_user(self):
        user = TestUserFactory()

        retrieved_user = user_get(user.id)
        
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.id, user.id)

    def test_user_get_nonexistent_user(self):
        user = user_get(9999)
        self.assertIsNone(user)

    def test_user_get_by_email_existing_user(self):
        TestUserFactory(email="test@example.com")
        retrieved_user = user_get_by_email("test@example.com")
        
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, "test@example.com")

    def test_user_get_by_email_nonexistent_user(self):
        user = user_get_by_email("nonexistent@example.com")
        self.assertIsNone(user)