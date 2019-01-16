from django.db import models, IntegrityError
from django.conf import settings
from django.db.models.manager import BaseManager

from burl.redirects import utils
from burl.redirects.database import RoughCountQuerySet


class RedirectManager(BaseManager.from_queryset(RoughCountQuerySet)):
    pass


class Redirect(models.Model):
    url = models.URLField(verbose_name='URL')
    burl = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name='Brief URL')
    description = models.CharField(max_length=255, blank=True, help_text='description of the destination URL')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    random = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)
    objects = RedirectManager()

    def __str__(self):
        return '/{} → {}'.format(self.burl, self.url)

    @classmethod
    def from_db(cls, db, field_names, values):
        """
        Override the from_db classmethod to add the loaded values from any
        existing record to the instance. See django docs on customizing model loading.
        """
        instance = super().from_db(db, field_names, values)
        instance._loaded_values = dict(zip(field_names, values))
        return instance

    def save(self, *args, **kwargs):
        """
        Override the default save method to enforce our BURL_BLACKLIST, a
        list of strings that we do not want to accidentally issue as hashids.

        :return: Redirect
        :rtype: burl.redirects.models.Redirect
        """
        if self.burl and hasattr(self, '_loaded_values'):
            if self.burl != self._loaded_values['burl']:
                self.random = False
        else:
            self.random = True
            self.burl = utils.make_burl(Redirect.objects.rough_count())
            # TODO add validator in serializer
            if self.burl in settings.BURL_BLACKLIST:
                self.burl = None
                return self.save(*args, **kwargs)
            try:
                return super().save(*args, **kwargs)
            except IntegrityError:
                self.burl = None
                return self.save(*args, **kwargs)
        return super().save(*args, **kwargs)
