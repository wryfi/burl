from rest_framework_simplejwt.views import TokenObtainPairView

from burl.core.api.serializers import TokenObtainUserPairSerializer


class TokenObtainUserPairView(TokenObtainPairView):
    serializer_class = TokenObtainUserPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response
