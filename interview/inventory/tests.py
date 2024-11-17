from datetime import timedelta, timezone
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APIClient, APITestCase
from rest_framework import status

from interview.inventory.models import Inventory, InventoryLanguage, InventoryType



class InventoryTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.recent_days = 4

        # Create related objects
        language = InventoryLanguage.objects.create(name='English')
        inventory_type = InventoryType.objects.create(name='Type 1')

        # Create test data
        self.test_objects = [Inventory.objects.create(name=f'Item {i}', metadata={}, language=language, type=inventory_type) for i in range(1, 9)]

    def test_no_params(self):
        url = reverse('inventory-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()['results']
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]['name'], 'Item 1')
        self.assertEqual(results[1]['name'], 'Item 2')
        self.assertEqual(results[2]['name'], 'Item 3')

    def test_limit_one(self):
        url = reverse('inventory-list')
        response = self.client.get(url, QUERY_STRING="limit=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'Item 1')

    def test_limit_hundred(self):
        url = reverse('inventory-list')
        response = self.client.get(url, QUERY_STRING="limit=100")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()['results']
        self.assertEqual(len(results), 8)
        self.assertEqual(results[0]['name'], 'Item 1')

    def test_offset_one(self):
        url = reverse('inventory-list')
        response = self.client.get(url, QUERY_STRING="offset=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()['results']
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]['name'], 'Item 2')
        self.assertEqual(results[1]['name'], 'Item 3')
        self.assertEqual(results[2]['name'], 'Item 4')

    def test_end_of_list(self):
        url = reverse('inventory-list')
        response = self.client.get(url, QUERY_STRING="offset=7&limit=5")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'Item 8')