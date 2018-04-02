"""hashurl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/redirects/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.redirects import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.redirects'))
"""
from django.contrib import admin
from django.urls import include, path

from hashurl.core.api import views as api_views
from hashurl.redirects import views as urls_views
from . import api_v1

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_views.root, name='api-root'),
    path('api/v1/', include(api_v1, namespace='api_v1')),
    path('<str:hashid>/', urls_views.redirect_hash)
]
