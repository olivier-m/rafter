# -*- coding: utf-8 -*-
"""
Exceptions
----------

.. autoexception:: ApiError

    .. autoattribute:: data
    .. automethod:: to_primitive


Error Handlers
--------------

.. autoclass:: ExceptionHandler

    .. automethod:: __call__

.. autoclass:: SanicExceptionHandler

.. autoclass:: ApiErrorHandler

"""

import logging
import sys
import traceback

from sanic.exceptions import SanicException
from sanic.response import json

__all__ = ('ApiError',)

log = logging.getLogger(__name__)


class ApiError(SanicException):
    def __init__(self, message: str, status_code: int=500, **kwargs):
        """
        :param message: An error message
        :param status_code: The returned HTTP status code

        Any other keyword argument will be added to the error data and
        will be added to the return of
        :attr:`~rafter.exceptions.ApiError.data`.
        """
        super(ApiError, self).__init__(message, status_code=status_code)
        self._data = kwargs

    @property
    def data(self):
        """
        Returns the internal property ``_data``. It can be overriden by
        specialized inherited exceptions.
        """
        return self._data

    def to_primitive(self) -> dict:
        """
        This methods is called by the error handler :class:`ApiErrorHandler`
        and returns a dict of error data.
        """
        return self.data or {}


class ExceptionHandler(object):
    """
    A generic ``Exception`` handler.

    The callable returns a JSON response with structured error data.
    The original error message is never returned. Use any type of
    SanicException if you need to do so.
    """

    def __call__(self, request, exception):
        """
        If the data's status is superior or equal to 500, the exception
        is logged, and if the Rafter app runs in debug mode, the statck
        trace is also returned in the response.
        """
        data = self.get_data(request, exception)

        if data['status'] >= 500:
            log.exception(exception)
            if request.app.debug:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                data['stack'] = traceback.extract_tb(exc_traceback)

        return json(data, data['status'])

    def get_data(self, request, exception):
        data = {'status': 500,
                'message': 'An error occured.'}
        return data


class SanicExceptionHandler(ExceptionHandler):
    """
    ``SanicException`` handler.

    This handler returns the original error message in its data.
    """
    def get_data(self, request, exception):
        data = super(SanicExceptionHandler, self).get_data(request, exception)
        data.update({'status': getattr(exception, 'status_code', 500),
                    'message': str(exception)})
        return data


class ApiErrorHandler(SanicExceptionHandler):
    """
    :class:`ApiError` handler.

    This handler returns all error data returned by
    :func:`ApiError.to_primitive`.
    """
    def get_data(self, request, exception):
        data = super(ApiErrorHandler, self).get_data(request, exception)
        data.update(exception.to_primitive())
        return data


default_error_handlers = ((ApiError, ApiErrorHandler()),
                          (SanicException, SanicExceptionHandler()),
                          (Exception, ExceptionHandler()))
