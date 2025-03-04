from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.urls import reverse
from django.core.cache import cache

from parkings.models import Parking
from users.models import User

class ParkingApiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.admin = User.objects.create_superuser(
            email='admin@sociale.com', password='admin'
        )
        cls.active_user = User.objects.create_user(
            email='chillguy@sociale.com',
            password='ilovesociale',
            is_active=True,
            is_verified=True
        )

        cls.parking_data = {
            "name": "Parking",
            "capacity": 12,
            "area": {
                "type": "Polygon",
                "coordinates": [
                    [[19.896595, 50.008492], [19.897456, 50.009673], 
                     [19.895648, 50.009341], [19.896595, 50.008492]]
                ]
            }
        }
        Parking.objects.create(
            name="boundary",
            capacity=12,
            area={
                "type": "Polygon",
                "coordinates": [
                    [[19.867737, 49.999826], [19.831094, 50.013598], 
                     [19.906522, 50.034662], [19.931808, 49.981917], [19.867737, 49.999826]]
                ]
            }
        )
        cls.parking = Parking.objects.create(
            name="TempParking",
            area={
                "type": "Polygon",
                "coordinates": [
                    [[19.896595, 50.008492], [19.897456, 50.009673], 
                     [19.895648, 50.009341], [19.896595, 50.008492]]
                ]
            }
        )  
        cls.inactive_parking = Parking.objects.create(
            name="TempParking",
            area={
                "type": "Polygon",
                "coordinates": [
                    [[19.894835, 50.009293], [19.895590, 50.010333], 
                     [19.897441, 50.009824], [19.894835, 50.009293]]
                ]
            },
            is_active=False
        )  

    def tearDown(self):
        cache.clear()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def parking_create(self, data):
        url = reverse('parkings:create')
        return self.client.post(url, data=data, format='json')

    def test_parking_list_noauth(self):
        url = reverse('parkings:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_parking_list(self):
        url = reverse('parkings:list')
        self.authenticate(self.active_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        response = self.client.get(f'{url}?include_inactive=True')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_parking_list_including_inactive(self):
        url = reverse('parkings:list')
        self.authenticate(self.admin)
        response = self.client.get(url)
        response = self.client.get(f'{url}?include_inactive=True')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_parking_get(self):
        url = reverse('parkings:detail', args=[self.parking.id])
        self.authenticate(self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('area'), self.parking.area)

    def test_parking_get_nonexistent(self):
        url = reverse('parkings:detail', args=[000])
        self.authenticate(self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_parking_create_noauth(self):
        response = self.parking_create(self.parking_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_parking_create_by_user(self):
        """Active Users should't be able to create new parkings"""
        self.authenticate(self.active_user)
        response = self.parking_create(self.parking_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_parking_create_by_admin(self):
        self.authenticate(self.admin)
        response = self.parking_create(self.parking_data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_parking_create_duplicate_name(self):
        self.authenticate(self.admin)
        self.parking_create(self.parking_data)

        response = self.parking_create(self.parking_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_parking_create_invalid_area(self):
        self.authenticate(self.admin)
        invalid_data = {
            "name": "Invalid Parking",
            "capacity": 10,
            "area": {  # Incorrect format coords (not nested list)
                "type": "Polygon",
                "coordinates": [[19.896595, 50.008492], [19.897456, 50.009673], [19.895648, 50.009341], [19.896595, 50.008492]]
            }
        }
        response = self.parking_create(invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_parking_create_negative_capacity(self):
        self.authenticate(self.admin)

        invalid_data = {
            "name": "Negative Parking",
            "capacity": -12,
            "area": self.parking_data["area"]
        }
        response = self.parking_create(invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_parking_update(self):
        self.authenticate(self.admin)
        url = reverse('parkings:update', args=[self.parking.id])

        update_data ={
            "name": "UpdatedParking",
            "area": {
                "type": "Polygon",
                "coordinates": [
                    [[19.898263, 50.010333], [19.895659,50.010537], 
                     [19.896729,50.011653], [19.898263, 50.010333]]
                ]
            }
        }
        response = self.client.put(url, data=update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.parking.refresh_from_db()
        self.assertEqual(self.parking.name, update_data['name'])
        self.assertEqual(self.parking.area, update_data['area'])


    def test_parking_update_outside_boundaries(self):
        self.authenticate(self.admin)
        url = reverse('parkings:update', args=[self.parking.id])
        
        invalid_update_data = {
            "area": {
                "type": "Polygon",
                "coordinates": [
                    [[19.825235, 49.999686], [19.791530, 49.990296], 
                     [19.802390, 49.966935], [19.825235, 49.999686]]
                ]
            }
        }
        response = self.client.put(url, data=invalid_update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_parking_delete(self):
        self.authenticate(self.admin)
        url = reverse('parkings:delete', args=[self.parking.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Parking.objects.filter(id=self.parking.id).exists())
    
    def test_parking_delete_nonexistent(self):
        self.authenticate(self.admin)
        url = reverse('parkings:delete', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)