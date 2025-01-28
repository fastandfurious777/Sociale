from django.test import TestCase
from users.models import User
from users.services import user_create, user_update, user_delete
from .factories import TestUserFactory

class UserServicesTests(TestCase):
    def setUp(self):
        self.user = TestUserFactory.create()

    def test_user_create(self):
        password = 'johny123'
        user = user_create(
            email='johnym@google.com', 
            password=password, 
            first_name='Johny',
            last_name='Bugaj'
        )
        
        user.refresh_from_db()
        self.assertNotEqual(password, user.password)

    def test_user_update(self):
        updated_data = {"email": "updatedpork@gmail.com"}
        user = user_update(self.user.id, updated_data)
        self.user.refresh_from_db()
        self.assertEqual(user, self.user)
        self.assertEqual(user.email, "updatedpork@gmail.com")

        self.assertIsNone(user_update(self.user.id, {"invalid_field": "value"}))
        self.assertIsNone(user_update(999, {"username": "NonExistent"}))

    def test_user_delete(self):
        self.assertIn(self.user, User.objects.all())
        user_data = user_delete(self.user.id)
        self.assertEqual(user_data['id'], self.user.id)
        self.assertNotIn(self.user, User.objects.all())
        self.assertIsNone(user_delete(self.user.id))