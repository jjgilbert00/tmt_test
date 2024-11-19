from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from interview.order.models import Order
from django.utils import timezone
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage


class EmbargoedOrderViewTest(APITestCase):
    def setUp(self):
        inventory_type = InventoryType.objects.create(name='Test Type')
        inventory_language = InventoryLanguage.objects.create(name='Test Language')
        inventory = Inventory.objects.create(
            name='Test Inventory',
            type=inventory_type,
            language=inventory_language,
            metadata={}
        )
        self.nowdate = timezone.now().date() + timezone.timedelta(days=2)
        self.orders = [
            Order.objects.create(
                inventory=inventory,
                start_date=timezone.now().date(),
                embargo_date=timezone.now().date() + timezone.timedelta(days=1)
            ),
            Order.objects.create(
                inventory=inventory,
                start_date=timezone.now().date(),
                embargo_date=timezone.now().date() + timezone.timedelta(days=3)
            ),
            Order.objects.create(
                inventory=inventory,
                start_date=timezone.now().date(),
                embargo_date=timezone.now().date() + timezone.timedelta(days=5)
            ),
        ]

    def test_embargoed_orders_with_valid_date(self):
        url = reverse('embargoed-order')
        response = self.client.get(url, {'date': self.nowdate})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_embargoed_orders_with_no_date(self):
        url = reverse('embargoed-order')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'date is required.')

    def test_embargoed_orders_with_invalid_date(self):
        url = reverse('embargoed-order')
        response = self.client.get(url, {'date': 'invalid-date'})
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)
