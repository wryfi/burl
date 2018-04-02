from django.utils.functional import cached_property
from django.db import models
from django.conf import settings

from hashids import Hashids
from hashurl.redirects import utils


class Redirect(models.Model):
    url = models.URLField(verbose_name='URL')
    description = models.CharField(max_length=255, blank=True, help_text='description of the destination URL')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return '/{} ({})'.format(self.hashid, self.url)

    @property
    def hashid(self):
        return utils.hashid_encode(self.id)
