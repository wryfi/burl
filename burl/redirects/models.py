from django.db import models, IntegrityError
from django.conf import settings

from burl.redirects import utils


class Redirect(models.Model):
    url = models.URLField(verbose_name='URL')
    burl = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name='Brief URL')
    description = models.CharField(max_length=255, blank=True, help_text='description of the destination URL')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    random = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return '/{} > {}'.format(self.burl, self.url)

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
        if not self.burl:
            self.random = True
            self.burl = utils.make_burl(Redirect.objects.count())
            # TODO use validators for checking against blacklist (serializer and/or form)
            #if self.burl in settings.HASHID_BLACKLIST:
            #    self.burl = None
            #    return self.save(*args, **kwargs)
            try:
                return super(Redirect, self).save(*args, **kwargs)
            except IntegrityError:
                self.burl = None
                return self.save(*args, **kwargs)
        return super(Redirect, self).save(*args, **kwargs)
