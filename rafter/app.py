# -*- coding: utf-8 -*-
from functools import wraps
import logging

from sanic import Sanic

from .exceptions import default_error_handlers
from .filters import filter_validate_schemas, filter_validate_response
from .http import Request

log = logging.getLogger(__name__)

__all__ = ('Rafter',)


class Rafter(Sanic):
    """
    This class inherits Sanic's default ``Sanic`` class.
    It provides an instance of your app, to which you can add
    resources or regular Sanic routes.
    """

    default_filters = [
        filter_validate_schemas,
        filter_validate_response,
    ]
    """
    Default filters called on every resource route.
    """

    default_error_handlers = default_error_handlers
    """
    Default error handlers. It must be a list of tuples containing the
    exception type and a callable.
    """

    default_request_class = Request
    """
    The default request class. If changed, it must inherit from
    :class:`rafter.http.Request`.
    """

    def __init__(self, **kwargs):
        """
        .. note::
            Please refer to `Sanic API reference <sanic_ref_>`_
            for init arguments.
        """
        kwargs.setdefault('request_class', self.default_request_class)
        if not issubclass(kwargs['request_class'], Request):
            raise RuntimeError('request_class should inherit '
                               'rafter.http.Request class')

        super(Rafter, self).__init__(**kwargs)

        for e, f in self.default_error_handlers:
            self.error_handler.add(e, f)

    def resource(self, uri, methods=frozenset({'GET'}), **kwargs):
        """
        Decorates a function to be registered as a resource route.

        :param uri: path of the URL
        :param methods: list or tuple of methods allowed
        :param filters: List of callable that will filter request and
                        response data
        :param validators: List of callable added to the filter list.
        :param request_schema: Schema for request data
        :param response_schema: Schema for response data
        :param host:
        :param strict_slashes:
        :param stream:
        :param version:
        :param name: user defined route name for url_for

        :return: A decorated function
        """
        def decorator(f):
            self.add_resource(f, uri, methods, **kwargs)

        return decorator

    def add_resource(self, handler, uri, methods=frozenset({'GET'}),
                     filters: [callable]=default_filters,
                     validators: [callable]=[],
                     request_schema=None,
                     response_schema=None,
                     **kwargs):
        """
        Register a resource route.

        :param handler: function or class instance
        :param uri: path of the URL
        :param methods: list or tuple of methods allowed
        :param filters: List of callable that will filter request and
                        response data
        :param validators: List of callable added to the filter list.
        :param request_schema: Schema for request data
        :param response_schema: Schema for response data
        :param host:
        :param strict_slashes:
        :param stream:
        :param version:
        :param name: user defined route name for url_for

        :return: function or class instance
        """

        filter_list = filters + validators
        filter_options = {
            'request_schema': request_schema,
            'response_schema': response_schema
        }
        filter_options.update(kwargs)

        handler = self.init_filters(filter_list, filter_options)(handler)
        return self.add_route(handler, uri, methods, **kwargs)

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
