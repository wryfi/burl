from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from burl.redirects.models import Redirect


class RedirectsApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.amy = get_user_model().objects.create_user('amy')
        cls.kif = get_user_model().objects.create_user('kif')
        cls.bender = get_user_model().objects.create_user('bender', is_superuser=True)
        Token.objects.create(user=cls.amy)
        Token.objects.create(user=cls.kif)
        Token.objects.create(user=cls.bender)

    def setUp(self):
        self.url = 'https://google.com'
        self.list_create_url = reverse('api_v1:redirects:redirect-list')

    def test_create_random_redirect(self):
        data = {'url': self.url, 'description': 'test1'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.amy.auth_token.key}')
        post = self.client.post(self.list_create_url, data, format='json')
        self.assertEquals(post.status_code, 201)
        redirect = Redirect.objects.get(burl=post.json()['burl'])
        self.assertEquals(redirect.user.id, self.amy.id)
        self.assertEquals(redirect.burl, post.json()['burl'])
        self.assertEquals(redirect.url, 'https://google.com')
        self.assertEquals(redirect.description, 'test1')
        self.assertTrue(redirect.enabled)

    def test_create_random_redirect_no_auth(self):
        data = {'url': 'https://google.com', 'user': self.kif.id}
        post = self.client.post(self.list_create_url, data, format='json')
        self.assertEquals(post.status_code, 403)

    def test_create_random_redirect_wrong_user(self):
        data = {'url': 'https://google.com', 'user': self.kif.id}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.amy.auth_token.key}')
        post = self.client.post(self.list_create_url, data, format='json')
        self.assertEquals(post.status_code, 201)
        self.assertEquals(post.json()['user'], str(self.amy.id))

    def test_create_specific_redirect(self):
        data = {'url': self.url, 'description': 'test1', 'burl': 'burl_test_1'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.amy.auth_token.key}')
        post = self.client.post(self.list_create_url, data, format='json')
        self.assertEquals(post.status_code, 201)
        redirect = Redirect.objects.get(burl='burl_test_1')
        self.assertEquals(redirect.user.id, self.amy.id)
        self.assertEquals(redirect.burl, 'burl_test_1')
        self.assertEquals(redirect.url, 'https://google.com')
        self.assertEquals(redirect.description, 'test1')
        self.assertTrue(redirect.enabled)

    def test_create_redirect_superuser(self):
        data = {'url': self.url, 'description': 'test1', 'burl': 'burl_test_1', 'user': str(self.amy.id)}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.bender.auth_token.key}')
        post = self.client.post(self.list_create_url, data, format='json')
        self.assertEquals(post.status_code, 201)
        self.assertEquals(post.json()['user'], str(self.amy.id))

    def test_create_blacklisted_redirect(self):
        data = {'url': self.url, 'description': 'test1', 'burl': 'admin'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.amy.auth_token.key}')
        post = self.client.post(self.list_create_url, data, format='json')
        self.assertEquals(post.status_code, 400)

    def test_read_redirect(self):
        redirect = Redirect.objects.create(user=self.amy, url=self.url, description='hello, world!')
        url = reverse('api_v1:redirects:redirect-detail', kwargs={'burl': redirect.burl})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.amy.auth_token.key}')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(redirect.burl, response.json()['burl'])
        self.assertEquals(str(redirect.user.id), response.json()['user'])
        self.assertEquals(redirect.description, response.json()['description'])
        self.assertEquals(redirect.url, response.json()['url'])

    def test_read_redirect_wrong_user(self):
        redirect = Redirect.objects.create(user=self.amy, url=self.url)
        url = reverse('api_v1:redirects:redirect-detail', kwargs={'burl': redirect.burl})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.kif.auth_token.key}')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_read_redirect_no_auth(self):
        redirect = Redirect.objects.create(user=self.amy, url=self.url)
        url = reverse('api_v1:redirects:redirect-detail', kwargs={'burl': redirect.burl})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_read_redirect_superuser(self):
        redirect = Redirect.objects.create(user=self.amy, url=self.url)
        url = reverse('api_v1:redirects:redirect-detail', kwargs={'burl': redirect.burl})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.bender.auth_token.key}')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['user'], str(redirect.user.id))

    def test_read_redirect_list(self):
        Redirect.objects.create(user=self.amy, url=self.url)
        Redirect.objects.create(user=self.kif, url=self.url)
        url = reverse('api_v1:redirects:redirect-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.amy.auth_token.key}')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()['results']), 1)
        self.assertEquals(response.json()['results'][0]['user'], str(self.amy.id))

    def test_read_redirect_list_no_auth(self):
        Redirect.objects.create(user=self.amy, url=self.url)
        url = reverse('api_v1:redirects:redirect-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_read_redirect_list_superuser(self):
        Redirect.objects.create(user=self.amy, url=self.url)
        Redirect.objects.create(user=self.kif, url=self.url)
        url = reverse('api_v1:redirects:redirect-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.bender.auth_token.key}')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()['results']), 2)
        users = [result['user'] for result in response.json()['results']]
        self.assertIn(str(self.amy.id), users)
        self.assertIn(str(self.kif.id), users)

    def test_update_redirect(self):
        redirect = Redirect.objects.create(user=self.amy, url=self.url)
        data = {'url': 'https://twitter.com', 'description': 'twitter', 'burl': 'twitter'}
        url = reverse('api_v1:redirects:redirect-detail', kwargs={'burl': redirect.burl})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.amy.auth_token.key}')
        put = self.client.put(url, data, format='json')
        self.assertEquals(put.status_code, 200)
        redirect.refresh_from_db()
        self.assertEquals(redirect.url, 'https://twitter.com')
        self.assertEquals(redirect.description, 'twitter')
        self.assertEquals(redirect.burl, 'twitter')

    def test_update_redirect_wrong_user(self):
        redirect = Redirect.objects.create(user=self.kif, url=self.url)
        data = {'url': 'https://facebook.com', 'description': 'friendface', 'burl': 'zuck'}
        url = reverse('api_v1:redirects:redirect-detail', kwargs={'burl': redirect.burl})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.amy.auth_token.key}')
        put = self.client.put(url, data, format='json')
        self.assertEquals(put.status_code, 404)

    def test_update_redirect_no_auth(self):
        redirect = Redirect.objects.create(user=self.kif, url=self.url)
        data = {'url': 'https://facebook.com', 'description': 'friendface', 'burl': 'zuck'}
        url = reverse('api_v1:redirects:redirect-detail', kwargs={'burl': redirect.burl})
        put = self.client.put(url, data, format='json')
        self.assertEquals(put.status_code, 403)

    def test_udpate_redirect_superuser(self):
        redirect = Redirect.objects.create(user=self.kif, url=self.url)
        data = {'url': 'https://facebook.com', 'description': 'friendface', 'burl': 'zuck', 'user': str(self.amy.id)}
        url = reverse('api_v1:redirects:redirect-detail', kwargs={'burl': redirect.burl})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.bender.auth_token.key}')
        put = self.client.put(url, data, format='json')
        self.assertEquals(put.status_code, 200)
        redirect.refresh_from_db()
        self.assertEquals(redirect.burl, 'zuck')
        self.assertEquals(redirect.description, 'friendface')
        self.assertEquals(redirect.url, 'https://facebook.com')
        self.assertEquals(redirect.user, self.amy)

    def test_delete_redirect(self):
        redirect = Redirect.objects.create(user=self.kif, url=self.url)
        url = reverse('api_v1:redirects:redirect-detail', kwargs={'burl': redirect.burl})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.kif.auth_token.key}')
        delete = self.client.delete(url)
        self.assertEquals(delete.status_code, 204)
        self.assertEquals(len(Redirect.objects.filter(burl=redirect.burl)), 0)

    def test_delete_redirect_wrong_user(self):
        redirect = Redirect.objects.create(user=self.kif, url=self.url)
        url = reverse('api_v1:redirects:redirect-detail', kwargs={'burl': redirect.burl})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.amy.auth_token.key}')
        delete = self.client.delete(url)
        self.assertEquals(delete.status_code, 404)
        self.assertEquals(len(Redirect.objects.filter(burl=redirect.burl)), 1)

    def test_delete_redirect_no_auth(self):
        redirect = Redirect.objects.create(user=self.amy, url=self.url)
        url = reverse('api_v1:redirects:redirect-detail', kwargs={'burl': redirect.burl})
        delete = self.client.delete(url)
        self.assertEquals(delete.status_code, 403)
        self.assertEquals(len(Redirect.objects.filter(burl=redirect.burl)), 1)

    def test_delete_redirect_superuser(self):
        redirect = Redirect.objects.create(user=self.amy, url=self.url)
        url = reverse('api_v1:redirects:redirect-detail', kwargs={'burl': redirect.burl})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.bender.auth_token.key}')
        delete = self.client.delete(url)
        self.assertEquals(delete.status_code, 204)
        self.assertEquals(len(Redirect.objects.filter(burl=redirect.burl)), 0)
