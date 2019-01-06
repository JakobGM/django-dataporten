import logging

import requests
import requests_cache

from django.conf import settings
from django.http import HttpResponse, HttpRequest
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

from .api import usergroups
from .models import DataportenUser

# Cache requests for 15 minutes
if settings.DATAPORTEN_CACHE_REQUESTS:
    requests_cache.install_cache(
        settings.DATAPORTEN_CACHE_PATH + 'dataporten_cache',
        backend='sqlite',
        expire_after=900,
        allowable_codes=(200,),
        include_get_headers=True,
    )


class DataportenGroupsMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        if DataportenUser.valid_request(request):
            request.user.__class__ = DataportenUser
