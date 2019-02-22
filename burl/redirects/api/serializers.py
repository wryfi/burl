from rest_framework import serializers

from burl.redirects.models import Redirect


class RedirectSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(required=False, source='user.id')

    class Meta:
        model = Redirect
        fields = ('burl', 'url', 'user', 'description', 'enabled')
