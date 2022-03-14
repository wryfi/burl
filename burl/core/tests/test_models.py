from django.test import TestCase
from django.contrib.auth import get_user_model

import uuid


class BurlUserTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("farnsworth")

    def test_user_uuid(self):
        self.assertIsInstance(self.user.id, uuid.UUID)
