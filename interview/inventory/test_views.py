from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from interview.inventory.models import Inventory, InventoryLanguage, InventoryType
from django.utils import timezone
from datetime import timedelta

class InventoryListByDateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.recent_days = 4

        # Create related objects
        language = InventoryLanguage.objects.create(name='English')
        inventory_type = InventoryType.objects.create(name='Type 1')

        # Create test data
        self.test_objects = [Inventory.objects.create(name=f'Item {i}', metadata={}, language=language, type=inventory_type) for i in range(1, 9)]
        for i in range(len(self.test_objects)):
            self.test_objects[i].created_at = (timezone.now() - timedelta(days=i + 1)).astimezone(timezone.utc)
            self.test_objects[i].save()
            self.test_objects[i].refresh_from_db()

    def test_inventory_list_by_date(self):
        url = reverse('inventory-list-by-date', kwargs={'date': (timezone.now() - timedelta(days=self.recent_days)).astimezone(timezone.utc).date()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.recent_days)
        self.assertEqual(response.data[-1]['name'], f'Item {self.recent_days}')

