from datetime import datetime

from django.db import IntegrityError
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.conf import settings

from burl.redirects.models import Redirect


class RedirectModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user('leela')
        cls.url = 'https://google.com'
        cls.description = 'test redirect'

    def test_create_redirect_random_burl(self):
        redirect = Redirect.objects.create(url=self.url, description=self.description, user=self.user)
        self.assertIsInstance(redirect, Redirect)
        self.assertEquals(redirect.url, 'https://google.com')
        self.assertIsInstance(redirect.burl, str)
        self.assertEquals(redirect.description, 'test redirect')
        self.assertIsInstance(redirect.created, datetime)
        self.assertIsInstance(redirect.created, datetime)
        self.assertTrue(redirect.enabled)

    def test_create_redirect_custom_burl(self):
        redirect = Redirect.objects.create(url=self.url, description=self.description, user=self.user, burl='google')
        self.assertIsInstance(redirect, Redirect)
        self.assertEquals(redirect.url, 'https://google.com')
        self.assertEquals(redirect.burl, 'google')
        self.assertEquals(redirect.description, 'test redirect')
        self.assertIsInstance(redirect.created, datetime)
        self.assertIsInstance(redirect.created, datetime)
        self.assertTrue(redirect.enabled)

    def test_create_redirect_custom_blacklisted_burl(self):
        with self.assertRaises(ValidationError):
            Redirect.objects.create(user=self.user, url=self.url, burl='admin')

    def test_create_redirect_custom_duplicate_burl(self):
        Redirect.objects.create(url=self.url, user=self.user, burl='test_duplicate')
        with self.assertRaises(IntegrityError):
            Redirect.objects.create(url=self.url, user=self.user, burl='test_duplicate')


class RedirectManagerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.min = settings.ROUGH_COUNT_MIN - 100
        cls.max = settings.ROUGH_COUNT_MIN + 1000
        cls.user = get_user_model().objects.create_user('hermes')
        cls.url = 'https://google.com'
        count = 0
        while count < cls.min:
            Redirect.objects.create(user=cls.user, url=cls.url)
            count += 1

    def test_rough_count_under_min(self):
        self.assertIsInstance(Redirect.objects.count(), int)
        self.assertIsInstance(Redirect.objects.rough_count(), int)
        self.assertEquals(Redirect.objects.count(), Redirect.objects.rough_count())

    def test_rough_count_over_min(self):
        count = Redirect.objects.count()
        while self.max - count > 0:
            Redirect.objects.create(user=self.user, url=self.url)
            count += 1
        count = Redirect.objects.count()
        rough_count = Redirect.objects.rough_count()
        self.assertIsInstance(count, int)
        self.assertIsInstance(rough_count, int)
        self.assertTrue(abs(count - rough_count) < count * 0.5)
