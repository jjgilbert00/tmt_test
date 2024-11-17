from django.test import TestCase
from .models import UserProfile


class UserProfileTestCase(TestCase):
    def setUp(self):
        UserProfile.objects.create(username="foo", first_name="Fred", last_name="Armisen", email="foo@foo.com")
        UserProfile.objects.create(username="bar", first_name="Brad", last_name="Pitt", email="bar@bar.com")

    def test_get_full_name(self):
        foo = UserProfile.objects.get(email="foo@foo.com")
        bar = UserProfile.objects.get(email="bar@bar.com")
        
        self.assertEqual(foo.get_full_name(), 'Fred Armisen')
        self.assertEqual(bar.get_full_name(), 'Brad Pitt')

    def test_get_username(self):
        foo = UserProfile.objects.get(email="foo@foo.com")
        bar = UserProfile.objects.get(email="bar@bar.com")
        
        # The email is the username
        self.assertEqual(foo.get_username(), 'foo@foo.com')
        self.assertEqual(bar.get_username(), 'bar@bar.com')

    def test_is_authenticated(self):
        foo = UserProfile.objects.get(email="foo@foo.com")
        bar = UserProfile.objects.get(email="bar@bar.com")
        
        # Defaults to True
        self.assertTrue(foo.is_authenticated)
        self.assertTrue(bar.is_authenticated)
