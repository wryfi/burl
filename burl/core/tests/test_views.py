from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.sites.models import Site
from django.test import TestCase

from django_burl.models import BriefURL, BriefURLDomainUser, BriefURLDefaultRedirect


class BurlCoreViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Site.objects.filter(id=1).update(domain="testserver", name="testserver")
        cls.site = Site.objects.get(id=1)
        cls.amy = get_user_model().objects.create_user("amy")
        BriefURLDomainUser.objects.create(
            site=cls.site, user=cls.amy, role=BriefURLDomainUser.Role.ADMIN
        )
        cls.burl = BriefURL.objects.create(
            url="https://arstechnica.com", site=cls.site, user=cls.amy
        )

    def test_root_redirect_settings_default(self):
        response = self.client.get("/")
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.headers["Location"], settings.DEFAULT_REDIRECT_URL)

    def test_root_redirect_db_default(self):
        BriefURLDefaultRedirect.objects.create(
            site=self.site, url="https://www.nytimes.com"
        )
        response = self.client.get("/")
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.headers["Location"], "https://www.nytimes.com")

    def test_redirect(self):
        response = self.client.get(f"/{self.burl.burl}/")
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.headers["Location"], "https://arstechnica.com")

    def test_api_root(self):
        response = self.client.get("/api/")
        self.assertEquals(response.status_code, 200)
        self.assertTrue("v1" in response.json())
        self.assertTrue("v2" in response.json())

    def test_api_v2_root(self):
        response = self.client.get("/api/v2/")
        self.assertEquals(response.status_code, 200)
        self.assertTrue("burls" in response.json())
        self.assertTrue("token" in response.json())

    def test_api_v2_burls(self):
        response = self.client.get("/api/v2/burls/")
        self.assertEquals(response.status_code, 401)
        self.assertEquals(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_api_v2_token_root(self):
        response = self.client.get("/api/v2/token/")
        self.assertEquals(response.status_code, 200)
        self.assertTrue("auth" in response.json())
        self.assertTrue("refresh" in response.json())
        self.assertTrue("verify" in response.json())
