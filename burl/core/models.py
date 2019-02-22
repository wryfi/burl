import uuid

from django.contrib.auth.models import AbstractUser
from django.db.models import UUIDField


class BurlUser(AbstractUser):
    id = UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
