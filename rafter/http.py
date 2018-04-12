# -*- coding: utf-8 -*-
"""
.. autoclass:: rafter.http.Request

.. autoclass:: rafter.http.Response
"""

from sanic.request import Request as BaseRequest
from sanic.response import HTTPResponse, json_dumps

__all__ = ('Response',)


class Request(BaseRequest):
    """
    This class is the default :class:`rafter.app.Rafter`'s request object
    that will be transmitted to every route. It adds a ``validated``
    attribute that will contains all of the validated values, if the route
    uses schemas.

    .. py:attribute:: validated

            This property can contain the request data after validation
            and conversion by the filter.
    """

    def __init__(self, *args, **kwargs):
        super(Request, self).__init__(*args, **kwargs)

        self.validated = {}


class Response(HTTPResponse):
    """
    A response object that you can return in any route. It looks a lot like
    ``sanic.response.json`` function except that instead of immediately
    serialize the data, it just keeps the value.
    Serialization (to JSON) will only happen when the response's body
    is retrieved.

    Example:

    .. code-block:: python
        :emphasize-lines: 3

        @app.resource('/')
        def main_route(request):
            return Response({'data': 'some data'})
    """

    def __init__(self, body=None, status=200, headers=None,
                 content_type='application/json'):
        """
        :param body: The data this will be serialized in response.
        :param status: The response status code.
        :param headers: Additionnal headers.
        :param content_type: Response MIME Type

        .. important::
            Input ``body`` will later be serialized. Its value is held by
            the internal ``_data`` attribute.
            Settings the ``body`` value will set this internal data but
            getting ``body`` will return the serialized value. This is the
            only way we can force Sanic HTTPResponse to serialize our response
            as late as possible.
        """
        super(Response, self).__init__(body=None, status=status,
                                       headers=headers,
                                       content_type=content_type)
        self._data = body

    @property
    def body(self):
        return self._encode_body(json_dumps(self._data))

    @body.setter
    def body(self, data):
        self._data = data

    @property
    def data(self):
        return self._data
