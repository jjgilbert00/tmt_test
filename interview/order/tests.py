from django.urls import reverse
from rest_framework.test import APITestCase
from interview.order.models import Order, OrderTag
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage


class TagListTests(APITestCase):

    def setUp(self):
        inventory_lang = InventoryLanguage.objects.create(name="english")
        inventory_type = InventoryType.objects.create(name="episode")
        inventory = Inventory.objects.create(type=inventory_type, language=inventory_lang, metadata={})
        foo = OrderTag.objects.create(name="Foo")
        bar = OrderTag.objects.create(name="Bar")
        baz = OrderTag.objects.create(name="Baz")
        self.foobar = Order.objects.create(inventory=inventory, embargo_date="2019-09-10", start_date="2019-09-09")
        self.foobar.tags.set([foo, bar])
        self.foobar.save()
        self.foobaz = Order.objects.create(inventory=inventory, embargo_date="2019-09-10", start_date="2019-09-09")
        self.foobaz.tags.set([foo, baz])
        self.foobaz.save()
        self.foobarbaz = Order.objects.create(inventory=inventory, embargo_date="2019-09-10", start_date="2019-09-09")
        self.foobarbaz.tags.set([foo, bar, baz])
        self.foobarbaz.save()

    def test_tags_by_order(self):
        """
        Query for tags associated with a given order.
        """
        url = reverse('order-detail')
        response = self.client.get(url, QUERY_STRING=f"order_id={self.foobar.id}")
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['name'], 'Foo')
        self.assertEqual(results[1]['name'], 'Bar')
        
        response = self.client.get(url, QUERY_STRING=f"order_id={self.foobaz.id}")
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['name'], 'Foo')
        self.assertEqual(results[1]['name'], 'Baz')
        
        response = self.client.get(url, QUERY_STRING=f"order_id={self.foobarbaz.id}")
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]['name'], 'Foo')
        self.assertEqual(results[1]['name'], 'Bar')
        self.assertEqual(results[2]['name'], 'Baz')

    def test_bad_order_id(self):
        """
        Query for tags with a nonexistent order id.
        """
        url = reverse('order-detail')
        response = self.client.get(url, QUERY_STRING=f"order_id=-1")
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertEqual(len(results), 0)