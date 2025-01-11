from users.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.core.cache import cache


class UserApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser(
            email='admin@sociale.com',
            password='admin'
        )
        cls.active_user = User.objects.create_user(
            email='chillguy@sociale.com',
            password='ilovesociale',
            is_active=True,
            is_verified=True
        )
        cls.random_user = User.objects.create_user(
            email='randomguy@random.com',
            password='randompass',
        )
        cls.client = APIClient()

    def tearDown(self):
        cache.clear()

    def login(self, email, password):
        url = reverse('users:login')
        return self.client.post(url, {'email': email, 'password': password})

    def test_user_login(self):
        response = self.login('chillguy@sociale.com', 'ilovesociale')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_brute_force(self):
        for _ in range(5):
            response = self.login('randomguy@random.com', 'wrongpass')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        response = self.login('randomguy@random.com', 'wrongpass')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def auth_admin(self):
        self.login('admin@sociale.com', 'admin')

    def auth_user(self):
        self.login('chillguy@sociale.com', 'ilovesociale')

    def test_user_list_admin(self):
        self.auth_admin()
        url = reverse('users:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_user_list_user(self):
        self.auth_user()
        url = reverse('users:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_detail(self):
        self.auth_admin()
        url = reverse('users:detail', args=[self.active_user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail_nonexistent(self):
        self.auth_admin()
        url = reverse('users:detail', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_register(self):
        url = reverse('users:register')
        data = {
            'email': 'validname@sociale.com',
            'first_name': 'Chill',
            'last_name': 'Guy',
            'password': 'StrongPass123',
            'confirmed_password': 'StrongPass123',
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=data['email'])
        self.assertFalse(user.is_verified)

    def test_register_existing_email(self):
        url = reverse('users:register')
        data = {
            'email': 'chillguy@sociale.com',
            'first_name': 'Chill',
            'last_name': 'Guy',
            'password': 'pass',
            'confirmed_password': 'pass',
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_password_mismatch(self):
        url = reverse('users:register')
        data = {
            'email': 'newuser@sociale.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'password123',
            'confirmed_password': 'password456',
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_update(self):
        self.auth_admin()
        url = reverse('users:update', args=[self.random_user.id])
        response = self.client.put(url, {'is_active': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.get(id=self.random_user.id).is_active)

    def test_admin_can_delete_user(self):
        self.auth_admin()
        url = reverse('users:delete', args=[self.random_user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.random_user.id).exists())

    def test_user_can_delete_user(self):
        self.auth_user()
        url = reverse('users:delete', args=[self.random_user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
