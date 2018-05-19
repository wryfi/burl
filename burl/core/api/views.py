from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def root(request, fmt=None):
    return Response({
        'v1': reverse('api_v1:root', request=request, format=fmt),
    })


@api_view(['GET'])
def v1_root(request, fmt=None):
    root_navigation = {
        'redirects': reverse('api_v1:redirects:redirect-list', request=request, format=fmt)
    }
    return Response(root_navigation)
