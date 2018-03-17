# -*- coding: utf-8 -*-
import logging
from operator import itemgetter
import sys
import traceback

from sanic.exceptions import SanicException
from sanic.response import json

__all__ = ('ApiError', 'ValidationErrors')

log = logging.getLogger(__name__)


def error_handler(request, exception):
    """
    A generic exception handler. Returns a JSON response
    with structured error data.
    """
    data = {'status': 500,
            'message': 'An error occured'}

    if isinstance(exception, SanicException):
        data.update({'status': getattr(exception, 'status_code', 500),
                     'message': str(exception)})

    if isinstance(exception, ApiError):
        data.update(exception.to_primitive())

    if data['status'] >= 500:
        log.exception(exception)
        if request.app.debug:  # pragma: nocover
            exc_type, exc_value, exc_traceback = sys.exc_info()
            data['stack'] = traceback.extract_tb(exc_traceback)

    return json(data, status=data['status'])


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
        This methods is called by the default error handler
        :func:`error_handler` and returns a dict of error data.
        """
        return self.data or {}


class ValidationErrors(ApiError):
    def __init__(self, errors: dict, **kwargs):
        super(ValidationErrors, self).__init__('Invalid input data', 400,
                                               **kwargs)
        self._errors = errors

    @property
    def data(self):
        """
        Returns a dictionnary containing all the passed data and an item
        ``error_list`` which holds the result of :attr:`error_list`.
        """
        res = {'error_list': self.error_list}
        res.update(super(ValidationErrors, self).data)
        return res

    @property
    def error_list(self):
        """
        Returns an error list based on the internal error dict values.
        Each item contains a dict with ``messages`` and ``path`` keys.

        Example::

            >>> errors = {
            >>>     'body': {
            >>>         'age': ['invalid age'],
            >>>         'options': {
            >>>             'extra': {
            >>>                 'ex1': ['invalid ex1'],
            >>>             }
            >>>         }
            >>>     }
            >>> }
            >>> e = ValidationErrors(errors)
            >>> e.error_list

            [
                {'messages': ['invalid age'],
                 'location': ['body', 'age']},
                {'messages': ['invalid ex1'],
                 'location': ['body', 'options', 'extra', 'ex1']},
            ]
        """
        return sorted(self._walk(self._errors), key=itemgetter('location'))

    def _walk(self, d, path=[]):
        nested_keys = tuple(k for k in d.keys() if isinstance(d[k], dict))
        items = tuple((k, d[k]) for k in d.keys() if k not in nested_keys)

        for p, v in items:
            yield {
                'location': path + [p],
                'messages': v
            }

        for k in nested_keys:
            for res in self._walk(d[k], path + [k]):
                yield res
