import logging

from django.http import HttpResponseRedirect
from django.conf import settings

from burl.redirects.models import Redirect


logger = logging.getLogger(__name__)


def redirect(request, burl):
    try:
        redirect = Redirect.objects.get(burl=burl)
    except Redirect.DoesNotExist:
        logger.error('failed to get redirect from burl {}'.format(burl))
        return HttpResponseRedirect(settings.DEFAULT_REDIRECT_URL)
    if redirect.enabled:
        return HttpResponseRedirect(redirect.url)
    else:
        return HttpResponseRedirect(settings.DEFAULT_REDIRECT_URL)
