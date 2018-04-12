# -*- coding: utf-8 -*-
"""
.. autofunction:: filter_validate_schemas
.. autofunction:: filter_validate_response
"""

from copy import deepcopy
import logging

from sanic.exceptions import abort
from sanic.request import RequestParameters
from sanic.response import HTTPResponse
from sanic.server import CIDict
from schematics.exceptions import BaseError
from schematics.types import ListType

from rafter.contrib.schematics.exceptions import ValidationErrors
from rafter.http import Response

log = logging.getLogger(__name__)

__all__ = ('filter_validate_schemas', 'filter_validate_response')


def filter_validate_schemas(get_response, params):
    """
    This filter validates input data against the resource's
    ``request_schema`` and fill the request's ``validated`` dict.

    Data from ``request.params`` and ``request.body`` (when the request body
    is of a form type) will be converted using the schema in order to get
    proper lists or unique values.

    .. important::
        The request validation is only effective when a
        ``request_schema`` has been provided by the resource definition.
    """

    request_schema = params.get('request_schema')

    if request_schema is None:
        return get_response

    def _convert_params(schema, data):
        for sc in schema.fields.values():
            name = sc.serialized_name or sc.name
            val = data.getlist(name)
            if val is None:
                continue

            if len(val) == 1 and not isinstance(sc, ListType):
                val = val[0]

            data[name] = val

    async def decorated_filter(request, *args, **kwargs):
        data = {
            'headers': CIDict(request.headers),
            'path': request.app.router.get(request)[2],
            'params': RequestParameters(request.args),
            'body': {}
        }

        if request.body:
            # Get body if we have something there
            if request.form:
                data['body'] = RequestParameters(request.form)
            else:
                # will raise 400 if cannot parse json
                data['body'] = deepcopy(request.json)

        if hasattr(request_schema, 'body') and request.form:
            _convert_params(request_schema.body, data['body'])

        if hasattr(request_schema, 'params') and data['params']:
            _convert_params(request_schema.params, data['params'])

        # Now, validate the whole thing
        try:
            model = request_schema(data, strict=False, validate=False)
            model.validate()
            request.validated = model.to_native()
        except BaseError as e:
            raise ValidationErrors(e.to_primitive())

        return await get_response(request, *args, **kwargs)

    return decorated_filter


def filter_validate_response(get_response, params):
    """
    This filter process the returned response. It does 2 things:

    - If the response is a ``sanic.response.HTTPResponse`` and not a
      :class:`rafter.http.Response`, return it immediately.
    - It processes, validates and serializes this response when a schema
      is provided.

    That means that you can always return a normal Sanic's HTTPResponse
    and thus, bypass the validation process when you need to do so.

    .. important::
        The response validation is only effective when:

        - A ``response_schema`` has been provided by the resource definition
        - The resource returns a :class:`rafter.http.Response` instance
          or arbitrary data.
    """

    schema = params.get('response_schema')

    async def decorated_filter(request, *args, **kwargs):
        response = await get_response(request, *args, **kwargs)

        if isinstance(response, HTTPResponse) and \
                not isinstance(response, Response):
            return response

        if not isinstance(response, Response):
            raise TypeError('response is not an instance '
                            'of rafter.http.Response.')

        if schema:
            data = {
                'body': response.data,
                'headers': response.headers
            }

            try:
                model = schema(data, strict=False, validate=False)
                model.validate()
                result = model.to_primitive()
                response.body = result.get('body', None)
                response.headers.update(result.get('headers', {}))
            except BaseError as e:
                log.exception(e)
                abort(500, 'Wrong data output')

        return response

    return decorated_filter
