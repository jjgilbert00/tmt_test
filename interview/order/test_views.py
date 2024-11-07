from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from interview.order.models import Order
from django.utils import timezone
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage

class DeactivateOrderViewTest(APITestCase):
    def setUp(self):
        inventory_type = InventoryType.objects.create(name='Test Type')
        inventory_language = InventoryLanguage.objects.create(name='Test Language')
        inventory = Inventory.objects.create(
            name='Test Inventory',
            type=inventory_type,
            language=inventory_language,
            metadata={}
        )
        self.order = Order.objects.create(
            inventory=inventory,
            start_date=timezone.now().date(),
            embargo_date=timezone.now().date() + timezone.timedelta(days=1)
        )

    def test_deactivate_order_success(self):
        url = reverse('deactivate-order', kwargs={'pk': self.order.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.order.refresh_from_db()
        self.assertFalse(self.order.is_active)

    def test_deactivate_order_not_found(self):
        url = reverse('deactivate-order', kwargs={'pk': 999})
        response = self.client.post(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)



