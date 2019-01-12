from django.contrib import admin
from django import forms
from django.utils.translation import gettext as _
from django.conf import settings
from django.core.exceptions import ValidationError

from burl.redirects.models import Redirect


class RedirectForm(forms.ModelForm):
    model = Redirect

    def clean_burl(self):
        burl = self.cleaned_data['burl']
        if burl in settings.BURL_BLACKLIST:
            raise ValidationError(_('The specified brief URL is blacklisted and cannot be used!'))
        return burl


class RedirectAdmin(admin.ModelAdmin):
    form = RedirectForm


admin.site.register(Redirect, RedirectAdmin)
