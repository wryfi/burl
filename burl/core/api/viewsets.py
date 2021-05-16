from rest_framework_simplejwt.views import TokenObtainPairView


class TokenCookieObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # TODO harden for production deployment
        response.set_cookie("burl_refresh_token", response.data["refresh"], max_age=14400, samesite="Lax",
                            domain=request.META["HTTP_HOST"].split(":")[0], httponly=True)
        return response
