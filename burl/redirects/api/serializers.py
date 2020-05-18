from django.conf import settings
from rest_framework import serializers

from burl.redirects.models import Redirect


class RedirectSerializer(serializers.ModelSerializer):
    user = serializers.UUIDField(required=False, source='user.id')

    class Meta:
        model = Redirect
        fields = ('burl', 'url', 'user', 'description', 'enabled', 'created', 'updated')

    def validate_burl(self, value):
        if value in settings.BURL_BLACKLIST:
            raise serializers.ValidationError(f'burl "{value}" is blacklisted by BURL_BLACKLIST setting')
        return value
