# -*- coding: utf-8 -*-
"""
.. autofunction:: filter_transform_response
"""

from sanic.response import HTTPResponse

from rafter.http import Response


def filter_transform_response(get_response, params):
    """
    This filter process the returned response. It does 3 things:

    - If the response is a ``sanic.response.HTTPResponse`` and not a
      :class:`rafter.http.Response`, return it immediately.
    - If the response is not a :class:`rafter.http.Response` instance,
      turn it to a :class:`rafter.http.Response` instance with the response
      as data.
    - Then, return the Response instance.

    As the Response instance is not immediately serialized, you can still
    validate its data without any serialization / de-serialization penalty.
    """

    async def decorated_filter(request, *args, **kwargs):
        response = await get_response(request, *args, **kwargs)

        if isinstance(response, HTTPResponse) and \
                not isinstance(response, Response):
            return response

        if not isinstance(response, Response):
            response = Response(response)

        return response

    return decorated_filter
