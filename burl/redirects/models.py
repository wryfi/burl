from django.db import models
from django.conf import settings

from burl.redirects import utils


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

    def save(self, *args, **kwargs):
        """
        Override the default save method to enforce our HASHID_BLACKLIST, a
        list of strings that we do not want to accidentally issue as hashids.
        In case of a collision, deleting the object and re-creating it gives
        it a new id (from which hashid is derived).

        :param args:
        :param kwargs:
        :return: Redirect
        """
        super(Redirect, self).save(*args, **kwargs)
        if self.hashid in settings.HASHID_BLACKLIST:
            self.delete()
            self.save()
        return self
