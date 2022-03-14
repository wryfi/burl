from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.urls import reverse
from rest_framework.test import APITestCase

from django_burl.models import BriefURL, BriefURLDomainUser


class BurlCoreApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Site.objects.filter(id=1).update(domain="testserver", name="testserver")
        cls.site = Site.objects.get(id=1)
        cls.url = "https://en.wikipedia.org/"
        cls.amy = get_user_model().objects.create_user("amy", password="amy54321")
        BriefURLDomainUser.objects.create(
            site=cls.site, user=cls.amy, role=BriefURLDomainUser.Role.ADMIN
        )
        cls.burl = BriefURL.objects.create(
            url="https://slashdot.org", user=cls.amy, site=cls.site
        )


class BurlCoreApiTestJWT(BurlCoreApiTestCase):
    def test_get_jwt_token(self):
        data = {"username": "amy", "password": "amy54321"}
        response = self.client.post(reverse("api_v2:token_auth"), data, format="json")
        self.assertEquals(response.status_code, 200)
        self.assertTrue("access" in response.json().keys())
        self.assertTrue("user" in response.json().keys())
        self.assertTrue("refresh" in response.json().keys())

    def test_use_jwt_token(self):
        data = {"username": "amy", "password": "amy54321"}
        response = self.client.post(reverse("api_v2:token_auth"), data, format="json")
        token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(
            reverse("api_v2:burls:burls-detail", kwargs={"burl": self.burl.burl}),
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()["burl"], self.burl.burl)
        self.assertEquals(response.json()["url"], self.burl.url)
