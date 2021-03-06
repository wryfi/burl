from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse


@api_view(['GET'])
def root(request, fmt=None):
    return Response({
        'v1': reverse('api_v1:root', request=request, format=fmt),
    })


@api_view(['GET'])
def v1_root(request, fmt=None):
    root_navigation = {
        'redirects': reverse('api_v1:redirects:redirect-list', request=request, format=fmt),
        'token': reverse('api_v1:token_root', request=request, format=fmt)
    }
    return Response(root_navigation)


@api_view(['get'])
def token_root(request, fmt=None):
    token_navigation = {
        'auth': reverse('api_v1:token_auth', request=request, format=fmt),
        'refresh': reverse('api_v1:token_refresh', request=request, format=fmt),
        'verify': reverse('api_v1:token_verify', request=request, format=fmt),
    }
    return Response(token_navigation)


