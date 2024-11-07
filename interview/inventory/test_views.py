from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from interview.inventory.models import Inventory
from datetime import datetime, timedelta

class InventoryListByDateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('inventory-list-by-date', kwargs={'date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')})
        
        # Create test data
        Inventory.objects.create(name='Item 2', created_at=datetime.now() - timedelta(days=3), metadata={}, language_id=1, type_id=0)
        Inventory.objects.create(name='Item 3', created_at=datetime.now() - timedelta(days=1), metadata={}, language_id=1, type_id=0)
        Inventory.objects.create(name='Item 1', created_at=datetime.now() - timedelta(days=5), metadata={}, language_id=1, type_id=0)

    def test_inventory_list_by_date(self):
        print(self.url)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Item 3')
