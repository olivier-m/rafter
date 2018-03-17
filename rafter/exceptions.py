# -*- coding: utf-8 -*-
from operator import itemgetter

from sanic.exceptions import SanicException

__all__ = ('ApiError', 'ValidationErrors')


class ApiError(SanicException):
    def __init__(self, message, status_code=500, **kwargs):
        super(ApiError, self).__init__(message, status_code=status_code)
        self._data = kwargs

    @property
    def data(self):
        return self._data

    def to_primitive(self):
        return self.data or {}


class ValidationErrors(ApiError):
    def __init__(self, errors, **kwargs):
        super(ValidationErrors, self).__init__('Invalid input data', 400,
                                               **kwargs)
        self._errors = errors

    @property
    def data(self):
        res = {'error_list': self.error_list}
        res.update(super(ValidationErrors, self).data)
        return res

    @property
    def error_list(self):
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
