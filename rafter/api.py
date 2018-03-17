# -*- coding: utf-8 -*-
from functools import wraps
import logging

from sanic import Sanic

from .filters import (filter_validate_schemas,
                      filter_validate_response,
                      filter_errors)
from .http import Request

log = logging.getLogger(__name__)

__all__ = ('App',)


class App(Sanic):
    default_request_class = Request
    default_filters = [
        filter_validate_schemas,
        filter_validate_response,
        filter_errors,
    ]

    def __init__(self, **kwargs):
        kwargs.setdefault('request_class', self.default_request_class)
        if not issubclass(kwargs['request_class'], Request):
            raise RuntimeError('request_class should inherit '
                               'rafter.http.Request class')

        super(App, self).__init__(**kwargs)

    def resource(self, uri, **kwargs):
        def decorator(f):
            self.add_resource(f, uri, **kwargs)

        return decorator

    def add_resource(self, handler, uri,
                     filters: [callable]=default_filters,
                     validators: [callable]=[],
                     request_schema=None,
                     response_schema=None,
                     **kwargs):

        filter_list = filters + validators
        filter_options = {
            'request_schema': request_schema,
            'response_schema': response_schema
        }
        filter_options.update(kwargs)

        handler = self.init_filters(filter_list, filter_options)(handler)
        return self.add_route(handler, uri, **kwargs)

    @staticmethod
    def init_filters(filter_list, params):
        def decorator(handler):
            get_response = handler
            for f in filter_list:
                get_response = f(get_response, params)

            @wraps(handler)
            async def wrapper(request, *args, **kwargs):
                return await get_response(request, *args, **kwargs)

            return wrapper
        return decorator
