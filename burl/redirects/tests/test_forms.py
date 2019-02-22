from django.contrib.auth import get_user_model
from django.test import TestCase

from burl.redirects import utils
from burl.redirects.models import Redirect
from burl.redirects.admin import RedirectAdminForm


class RedirectAdminFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user('zoidberg')
        cls.redirect = Redirect.objects.create(user=cls.user, url='https://google.com')

    def test_init(self):
        RedirectAdminForm(self.redirect)

    def test_blacklisted_burl(self):
        redirect = self.redirect.__dict__
        redirect['burl'] = 'admin'
        form = RedirectAdminForm(redirect)
        self.assertTrue('burl' in form.errors)
        self.assertFalse(form.is_valid())

    def test_valid_burl(self):
        redirect = self.redirect.__dict__
        redirect['burl'] = utils.make_burl(1000)
        redirect['url'] = 'https://google.com'
        redirect['user'] = self.user.id
        form = RedirectAdminForm(redirect)
        self.assertTrue(form.is_valid())
