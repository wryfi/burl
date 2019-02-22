from django.urls import include, path

from burl.core.api import views
from burl.redirects.api import urls_v1 as redirect_urls


app_name = 'api_v1'


urlpatterns = [
    path('', views.v1_root, name='root'),
    path('', include(redirect_urls))
]
