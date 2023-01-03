from rest_framework.renderers import BaseRenderer, JSONRenderer
from rest_framework import status
from .settings import swagger_settings as settings
from django.shortcuts import render, resolve_url
import json

class OpenAPIRenderer(BaseRenderer):
    media_type = 'application/openapi+json'
    charset = None
    format = 'openapi'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return JSONRenderer().render(data)

class SwaggerUIRenderer(BaseRenderer):
    media_type = 'text/html'
    format = 'swagger'
    template = 'swagger/index.html'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        self.set_context(data, renderer_context)
        return render(
            renderer_context['request'],
            self.template,
            renderer_context
        )

    def set_context(self, data, renderer_context):
        renderer_context['USE_SESSION_AUTH'] = \
            settings.USE_SESSION_AUTH
        renderer_context.update(self.get_auth_urls())

        drs_settings = self.get_ui_settings()
        renderer_context['drs_settings'] = json.dumps(drs_settings)
        renderer_context['spec'] = OpenAPIRenderer().render(
            data=data,
            renderer_context=renderer_context
        ).decode()

    def get_auth_urls(self):
        urls = {}
        if settings.LOGIN_URL is not None:
            urls['LOGIN_URL'] = resolve_url(settings.LOGIN_URL)
        if settings.LOGOUT_URL is not None:
            urls['LOGOUT_URL'] = resolve_url(settings.LOGOUT_URL)

        return urls

    def get_ui_settings(self):
        data = {
            'apisSorter': settings.APIS_SORTER,
            'docExpansion': settings.DOC_EXPANSION,
            'jsonEditor': settings.JSON_EDITOR,
            'operationsSorter': settings.OPERATIONS_SORTER,
            'showRequestHeaders': settings.SHOW_REQUEST_HEADERS,
            'supportedSubmitMethods': settings.SUPPORTED_SUBMIT_METHODS,
            'acceptHeaderVersion': settings.ACCEPT_HEADER_VERSION,
            'customHeaders': settings.CUSTOM_HEADERS,
        }
        if settings.VALIDATOR_URL != '':
            data['validatorUrl'] = settings.VALIDATOR_URL

        return data
