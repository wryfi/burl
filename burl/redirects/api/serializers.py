from rest_framework import serializers

from burl.redirects.models import Redirect


class RedirectSerializer(serializers.ModelSerializer):
    random = serializers.ReadOnlyField()

    class Meta:
        model = Redirect
        fields = ('id', 'url', 'burl', 'description', 'user', 'random', 'enabled')
