from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from django_burl.models import BriefURLDefaultRedirect


def root_redirect(request):
    redirect_to = settings.DEFAULT_REDIRECT_URL
    try:
        redirect_to = BriefURLDefaultRedirect.objects.get(site=request.site).url
    except ObjectDoesNotExist:
        pass
    return redirect(redirect_to)
