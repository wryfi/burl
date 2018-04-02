from rest_framework.viewsets import ModelViewSet

from hashurl.redirects.models import Redirect
from hashurl.redirects.api.serializers import RedirectSerializer


class RedirectViewSet(ModelViewSet):
    serializer_class = RedirectSerializer
    queryset = Redirect.objects.all()