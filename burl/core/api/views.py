from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(["GET"])
def root(request, fmt=None):
    return Response(
        {
            "v1": reverse("api_v1:root", request=request, format=fmt),
            "v2": reverse("api_v2:root", request=request, format=fmt),
        }
    )


@api_view(["GET"])
def v1_root(request, fmt=None):
    root_navigation = {
        "redirects": reverse(
            "api_v1:redirects:redirect-list", request=request, format=fmt
        ),
        "token": reverse("api_v1:token_root", request=request, format=fmt),
    }
    return Response(root_navigation)


@api_view(["GET"])
def v2_root(request, fmt=None):
    root_navigation = {
        "burls": reverse("api_v2:burls:burls-list", request=request, format=fmt),
        "token": reverse("api_v2:token_root", request=request, format=fmt),
    }
    return Response(root_navigation)


@api_view(["GET"])
def token_root(request, fmt=None):
    token_navigation = {
        "auth": reverse("api_v1:token_auth", request=request, format=fmt),
        "refresh": reverse("api_v1:token_refresh", request=request, format=fmt),
        "verify": reverse("api_v1:token_verify", request=request, format=fmt),
    }
    return Response(token_navigation)


@api_view(["GET"])
def v2_token_root(request, fmt=None):
    token_navigation = {
        "auth": reverse("api_v2:token_auth", request=request, format=fmt),
        "refresh": reverse("api_v2:token_refresh", request=request, format=fmt),
        "verify": reverse("api_v2:token_verify", request=request, format=fmt),
    }
    return Response(token_navigation)


@api_view(["POST"])
def token_refresh(request):
    token = request.COOKIES.get("burl_refresh_token")
    if token:
        refresh = RefreshToken(str(token))
        access = str(refresh.access_token)
        if access:
            return Response({"access": access}, 200)
        else:
            return Response({"unauthorized"}, 401)
    return Response("unauthorized", 401)


@api_view(["POST"])
def token_refresh_revoke(_request):
    response = Response("ok")
    response.delete_cookie("burl_refresh_token")
    return response
