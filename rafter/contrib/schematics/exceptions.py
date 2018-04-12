# -*- coding: utf-8 -*-
"""
.. autoexception:: ValidationErrors

    .. autoattribute:: data
    .. autoattribute:: error_list

"""

from operator import itemgetter

from rafter.exceptions import ApiError

__all__ = ('ValidationErrors',)


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
