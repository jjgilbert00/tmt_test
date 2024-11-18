from django.urls import reverse
from rest_framework.test import APITestCase
from interview.order.models import Order, OrderTag
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage


class OrdersByTagTestCase(APITestCase):

    def setUp(self):
        inventory_lang = InventoryLanguage.objects.create(name="english")
        inventory_type = InventoryType.objects.create(name="episode")
        inventory = Inventory.objects.create(type=inventory_type, language=inventory_lang, metadata={})
        self.foo = OrderTag.objects.create(name="Foo")
        self.bar = OrderTag.objects.create(name="Bar")
        self.baz = OrderTag.objects.create(name="Baz")
        self.foobar = Order.objects.create(inventory=inventory, embargo_date="2019-09-10", start_date="2019-09-09")
        self.foobar.tags.set([self.foo, self.bar])
        self.foobar.save()
        self.foobaz = Order.objects.create(inventory=inventory, embargo_date="2019-09-10", start_date="2019-09-09")
        self.foobaz.tags.set([self.foo, self.baz])
        self.foobaz.save()
        self.foobarbaz = Order.objects.create(inventory=inventory, embargo_date="2019-09-10", start_date="2019-09-09")
        self.foobarbaz.tags.set([self.foo, self.bar, self.baz])
        self.foobarbaz.save()

    def test_orders_by_tag_id(self):
        """
        Query for Orders associated with a given OrderTag's id.
        """
        url = reverse('orders-by-tag-id',  kwargs={'tag_id': self.foo.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertEqual(len(results), 3)
        self.assertContains(response, "Foo", 3, 200)

    def test_orders_with_fake_tag_id(self):
        """
        Query for Orders associated with a nonexistent OrderTag id.
        """
        url = reverse('orders-by-tag-id',  kwargs={'tag_id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertEqual(len(results), 0)

    def test_orders_by_tag_name(self):
        """
        Query for Orders associated with a given OrderTag's name.
        """
        url = reverse('orders-by-tag-name',  kwargs={'tag_name': self.baz.name})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertEqual(len(results), 2)
        self.assertContains(response, "Baz", 2, 200)

    def test_orders_with_fake_tag_name(self):
        """
        Query for Orders associated with a nonexistent OrderTag name.
        """
        url = reverse('orders-by-tag-name',  kwargs={'tag_name': "NOT_REAL"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertEqual(len(results), 0)


