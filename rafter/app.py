# -*- coding: utf-8 -*-
"""
.. autoclass:: Rafter
"""

from functools import wraps
import logging

from sanic import Sanic

from rafter.exceptions import default_error_handlers
from rafter.filters import filter_transform_response
from rafter.http import Request

log = logging.getLogger(__name__)

__all__ = ('Rafter',)


class Rafter(Sanic):
    """
    This class inherits Sanic's default ``Sanic`` class.
    It provides an instance of your app, to which you can add
    resources or regular Sanic routes.

    .. note::
        Please refer to `Sanic API reference <sanic_ref_>`_
        for init arguments.

    .. autoattribute:: default_filters
    .. autoattribute:: default_error_handlers
    .. autoattribute:: default_request_class

    .. automethod:: add_resource
    .. automethod:: resource
    """

    default_filters = [filter_transform_response]
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
        :param host:
        :param strict_slashes:
        :param stream:
        :param version:
        :param name: user defined route name for url_for
        :param filters: List of callable that will filter request and
                        response data
        :param validators: List of callable added to the filter list.

        :return: A decorated function
        """
        def decorator(f):
            if kwargs.get('stream'):
                f.is_stream = kwargs['stream']
            self.add_resource(f, uri=uri, methods=methods, **kwargs)

        return decorator

    def add_resource(self, handler, uri, methods=frozenset({'GET'}),
                     **kwargs):
        """
        Register a resource route.

        :param handler: function or class instance
        :param uri: path of the URL
        :param methods: list or tuple of methods allowed
        :param host:
        :param strict_slashes:
        :param version:
        :param name: user defined route name for url_for
        :param filters: List of callable that will filter request and
                        response data
        :param validators: List of callable added to the filter list.

        :return: function or class instance
        """

        sanic_args = ('host', 'strict_slashes', 'version', 'name')
        view_kwargs = dict((k, v) for k, v in kwargs.items()
                           if k in sanic_args)

        filters = kwargs.get('filters', self.default_filters)
        validators = kwargs.get('validators', [])

        filter_list = list(filters) + list(validators)
        filter_options = {
            'filter_list': filter_list,
            'handler': handler,
            'uri': uri,
            'methods': methods
        }
        filter_options.update(kwargs)

        handler = self.init_filters(filter_list, filter_options)(handler)
        return self.add_route(handler=handler, uri=uri, methods=methods,
                              **view_kwargs)

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
