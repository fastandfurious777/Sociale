from rest_framework import status
from django.urls import reverse
from utils.tests import CustomAPITestCase
from bikes.tests.factories import TestBikeFactory
from bikes.models import Bike


class BikeApiTests(CustomAPITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.setUpAuthData()
        cls.bike = TestBikeFactory.create(is_available=False)
        TestBikeFactory.create_batch(3, is_available=True)
        

    def test_bike_list(self):
        url = reverse("bikes:list")
        self.authenticate(self.active_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        self.authenticate(self.admin)
        response = self.client.get(f"{url}?include_unavailable=True")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    def test_bike_list_noauth(self):
        url = reverse("bikes:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.authenticate(self.verified_not_active_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bike_list_include_unavailable_noauth(self):
        url = reverse("bikes:list")
        self.authenticate(self.active_user)
        response = self.client.get(f"{url}?include_unavailable=True")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bike_get_noauth(self):
        url = reverse("bikes:detail", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bike_get(self):
        url = reverse("bikes:detail", args=[self.bike.id])
        self.authenticate(self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.bike.name, response.data.values())

    def test_bike_create(self):
        url = reverse("bikes:create")
        self.authenticate(self.admin)
        bike_data = {
            "name": "Marin",
            "lon": 2,
            "lat": 1,
            "code": 7812,
        }
        response = self.client.post(url, data=bike_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        bike = Bike.objects.get(name=bike_data["name"])
        self.assertEqual(bike.code, bike_data["code"])

    def test_bike_update(self):
        bike = Bike.objects.get(id=1)
        url = reverse("bikes:update", args=[bike.id])
        self.authenticate(self.admin)
        bike_data = {
            "lat": 3,
            "code": 1111,
        }
        response = self.client.put(url, data=bike_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        bike.refresh_from_db()
        self.assertEqual(bike.code, bike_data["code"])

    def test_bike_delete_noauth(self):
        url = reverse("bikes:delete", args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.authenticate(self.active_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bike_delete(self):
        self.authenticate(self.admin)
        url = reverse("bikes:delete", args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
