from rest_framework.decorators import renderer_classes, api_view, permission_classes
from .renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework import response, permissions
import yaml
from django.conf import settings

@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
@permission_classes([permissions.AllowAny])
def schema_view(request):
    with open("codetest/swagger/swagger.yaml", "rb") as swaggerdoc:
        data = swaggerdoc.read()

    overrided = yaml.load(data, Loader=yaml.FullLoader)
    overrided['host'] = request.META['HTTP_HOST']
    overrided['schemes'] = ['http']
    return response.Response(overrided)
