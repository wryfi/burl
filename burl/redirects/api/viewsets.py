from rest_framework.viewsets import ModelViewSet

from burl.redirects.models import Redirect
from burl.redirects.api.serializers import RedirectSerializer


class RedirectViewSet(ModelViewSet):
    serializer_class = RedirectSerializer
    queryset = Redirect.objects.all()