from rest_framework import routers
from django.urls import include, path

from burl.redirects.api import views, viewsets


router = routers.SimpleRouter()
router.register(r'redirects', viewsets.RedirectViewSet, base_name='redirect')


urlpatterns = [
    path('', views.api_root, name='redirects-root'),
    path('', include((router.urls, 'redirects')))
]