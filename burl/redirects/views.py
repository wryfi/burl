import logging

from django.conf import settings
from django.http import HttpResponseRedirect

from burl.redirects.models import Redirect
from burl.redirects import utils


logger = logging.getLogger(__name__)


def redirect_hash(request, hashid):
    try:
        url_id = utils.hashid_decode(hashid)[0]
        url = Redirect.objects.get(id=url_id)
    except Exception as ex:
        logger.error('failed to get redirect from hashid {}: {}'.format(hashid, ex))
        return HttpResponseRedirect(settings.DEFAULT_REDIRECT_URL)
    if url.enabled:
        return HttpResponseRedirect(url.url)
    else:
        return HttpResponseRedirect(settings.DEFAULT_REDIRECT_URL)
