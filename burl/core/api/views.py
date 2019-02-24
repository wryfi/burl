from django.urls import path, include

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.decorators import api_view
from rest_framework_swagger import renderers
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


class SwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        from burl.core.urls import api_v1
        api_url_patterns = [
            path('api/v1/', include(api_v1))
        ]
        generator = SchemaGenerator(title='burl api', patterns=api_url_patterns)
        schema = generator.get_schema(request=request)

        return Response(schema)
