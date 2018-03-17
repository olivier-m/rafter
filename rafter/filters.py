# -*- coding: utf-8 -*-
import logging
import sys
import traceback

from sanic.exceptions import SanicException, abort
from sanic.response import HTTPResponse, json
from schematics.exceptions import BaseError
from schematics.types import ListType

from .exceptions import ApiError, ValidationErrors
from .http import Response

log = logging.getLogger(__name__)


def filter_validate_schemas(get_response, params):
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

    async def md(request, *args, **kwargs):
        data = {
            'headers': request.headers,
            'path': request.app.router.get(request)[2],
            'params': request.args,
            'body': {}
        }

        if request.body:
            # Get body if we have something there
            # will raise 400 if cannot parse json
            data['body'] = request.form or request.json

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

    return md


def filter_validate_response(get_response, params):
    schema = params.get('response_schema')

    async def md(request, *args, **kwargs):
        response = await get_response(request, *args, **kwargs)

        if isinstance(response, HTTPResponse):
            return response

        if not isinstance(response, Response):
            response = Response(response)

        if schema:
            try:
                model = schema(response.data, strict=False, validate=False)
                model.validate()
                response.data = model.to_primitive()
            except BaseError as e:
                log.exception(e)
                abort(500, 'Wrong data output')

        return response.response()

    return md


def filter_errors(get_response, params):
    async def md(request, *args, **kwargs):
        try:
            return await get_response(request, *args, **kwargs)
        except Exception as e:
            data = {'status': 500,
                    'message': 'An error occured'}

            if isinstance(e, SanicException):
                data.update({'status': getattr(e, 'status_code', 500),
                             'message': str(e)})

            if isinstance(e, ApiError):
                data.update(e.to_primitive())

            if data['status'] >= 500:
                log.exception(e)
                if request.app.debug:  # pragma: nocover
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    data['stack'] = traceback.extract_tb(exc_traceback)

            return json(data, status=data['status'])

    return md
