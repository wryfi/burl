from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
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
    filterset_fields = {
        'enabled': ['exact'],
        'description': ['exact', 'icontains'],
        'created': ['exact', 'lt', 'gt', 'lte', 'gte'],
        'updated': ['exact', 'lt', 'gt', 'lte', 'gte'],
        'url': ['exact', 'icontains'],
        'burl': ['exact', 'icontains']
    }
    lookup_field = 'burl'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Redirect.objects.order_by('-created')
        elif self.request.user.is_authenticated:
            return Redirect.objects.filter(user=self.request.user).order_by('-created')
        else:
            return []

    def perform_create(self, serializer):
        if self.request.user.is_superuser and 'user' in serializer._validated_data.keys():
            user = get_object_or_404(get_user_model(), id=serializer._validated_data['user']['id'])
            serializer.save(user=user)
        else:
            serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.is_superuser and 'user' in serializer._validated_data.keys():
            user = get_object_or_404(get_user_model(), id=serializer._validated_data['user']['id'])
            serializer.save(user=user)
        else:
            serializer.save(user=self.request.user)

