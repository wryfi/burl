from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenVerifyView,
)

from burl.core.api import views
from burl.core.api.viewsets import TokenObtainUserPairView
from django_burl.api.v1 import urls as redirect_urls

app_name = "api_v1"

urlpatterns = [
    path("", views.v1_root, name="root"),
    path("", include(redirect_urls)),
    path("token/", views.token_root, name="token_root"),
    path("token/auth/", TokenObtainUserPairView.as_view(), name="token_auth"),
    path("token/refresh/", csrf_exempt(views.token_refresh), name="token_refresh"),
    path(
        "token/refresh/revoke/", views.token_refresh_revoke, name="token_refresh_revoke"
    ),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "swagger/",
        TemplateView.as_view(
            template_name="core/api/swagger.html",
            extra_context={"schema_url": "api_v1:openapi_schema"},
        ),
        name="swagger_ui",
    ),
    path(
        "openapi/",
        get_schema_view(
            title="burl api",
            description="rest api for burl",
            version="1",
            url="/api/v1",
            urlconf="burl.core.urls.api_v1",
        ),
        name="openapi_schema",
    ),
]
