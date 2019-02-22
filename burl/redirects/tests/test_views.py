from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from burl.redirects.models import Redirect


class RedirectViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user('fry')
        cls.redirect = Redirect.objects.create(user=cls.user, url='https://twitter.com')
        cls.redirect_disabled = Redirect.objects.create(user=cls.user, url='https://google.com', enabled=False)

    def test_redirect(self):
        url = reverse('redirect', kwargs={'burl': self.redirect.burl})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response._headers['location'][1], 'https://twitter.com')

    def test_redirect_not_found(self):
        url = reverse('redirect', kwargs={'burl': 'asdf1234'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_redirect_disabled(self):
        url = reverse('redirect', kwargs={'burl': self.redirect_disabled.burl})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
