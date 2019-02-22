from django.db.models.manager import BaseManager
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.conf import settings

from burl.redirects import utils
from burl.redirects.database import RoughCountQuerySet


class RedirectManager(BaseManager.from_queryset(RoughCountQuerySet)):
    pass


class Redirect(models.Model):
    url = models.URLField(max_length=2048, db_index=True, verbose_name='URL')
    burl = models.CharField(max_length=2048, unique=True, blank=True, db_index=True, verbose_name='Brief URL')
    description = models.CharField(max_length=255, blank=True, help_text='description of the destination URL')
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)
    objects = RedirectManager()

    def __str__(self):
        return f'/{self.burl} → {self.url}'

    def _save_burl(self):
        if self.burl:
            self.random = False
            # TODO add validator in serializer for user-supplied burls
            if self.burl in settings.BURL_BLACKLIST:
                raise ValidationError(f'burl "{self.burl}" is blacklisted by BURL_BLACKLIST setting')
        else:
            self.random = True
            self.burl = utils.make_burl(ceiling=Redirect.objects.rough_count())
            if self.burl in settings.BURL_BLACKLIST:
                self.burl = None
                return self._save_burl()

    def save(self, *args, **kwargs):
        self._save_burl()
        try:
            with transaction.atomic():
                return super().save(*args, **kwargs)
        except IntegrityError as ex:
            if 'unique constraint' in repr(ex):
                if self.random:
                    self.burl = None
                    return self.save(*args, **kwargs)
                else:
                    raise ex
