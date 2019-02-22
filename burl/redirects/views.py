import logging

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404

from burl.redirects.models import Redirect


logger = logging.getLogger(__name__)


def get_redirect(request, burl):
    redirect = get_object_or_404(Redirect, burl=burl)
    if redirect.enabled:
        return HttpResponseRedirect(redirect.url)
    else:
        raise Http404
