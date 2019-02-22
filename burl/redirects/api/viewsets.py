from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from burl.redirects.models import Redirect
from burl.redirects.api.serializers import RedirectSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.user == request.user


class RedirectViewSet(ModelViewSet):
    serializer_class = RedirectSerializer
    permission_classes = (IsOwner, IsAuthenticated)
    lookup_field = 'burl'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Redirect.objects.all()
        elif self.request.user.is_authenticated:
            return Redirect.objects.filter(user=self.request.user)
        else:
            return []

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
