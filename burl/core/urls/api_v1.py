from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

from burl.core.api import views
from burl.redirects.api import urls_v1 as redirect_urls

app_name = 'api_v1'

urlpatterns = [
    path('', views.v1_root, name='root'),
    path('', include(redirect_urls)),
    path('token/', views.token_root, name='token_root'),
    path('token/auth/', TokenObtainPairView.as_view(), name='token_auth'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('swagger/', TemplateView.as_view(
        template_name='core/api/swagger.html',
        extra_context={'schema_url': 'api_v1:openapi_schema'}
    ), name='swagger_ui'),
    path('openapi/', get_schema_view(
        title='burl api',
        description='rest api for burl',
        version='1',
    ), name='openapi_schema')
]
