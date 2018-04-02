from rest_framework import serializers

from hashurl.redirects.models import Redirect


class RedirectSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    def get_short_url(self, obj):
        return '/{}'.format(obj.hashid)

    class Meta:
        model = Redirect
        fields = ('id', 'url', 'description', 'enabled', 'user', 'short_url')
