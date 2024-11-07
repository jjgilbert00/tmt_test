from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from interview.inventory.models import Inventory, InventoryLanguage, InventoryType
from datetime import datetime, timedelta
from django.utils import timezone

class InventoryListByDateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('inventory-list-by-date', kwargs={'date': (timezone.now() - timedelta(days=1)).date()})
        
        # Create related objects
        language = InventoryLanguage.objects.create(name='English')
        inventory_type = InventoryType.objects.create(name='Type 1')
        
        # Create test data
        Inventory.objects.create(name='Item 2', created_at=(timezone.now() - timedelta(days=3)).date(), metadata={}, language=language, type=inventory_type)
        Inventory.objects.create(name='Item 3', created_at=(timezone.now() - timedelta(days=1)).date(), metadata={}, language=language, type=inventory_type)
        Inventory.objects.create(name='Item 1', created_at=(timezone.now() - timedelta(days=5)).date(), metadata={}, language=language, type=inventory_type)

    def test_inventory_list_by_date(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Item 3')
