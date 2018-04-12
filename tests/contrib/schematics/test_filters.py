# -*- coding: utf-8 -*-
import pytest

from sanic.exceptions import ServerError
from sanic.response import HTTPResponse
from sanic.server import CIDict
from schematics import Model, types

from rafter.app import Rafter
from rafter.contrib.schematics import ValidationErrors
from rafter.http import Response
from rafter.contrib.schematics import (
    model_node, filter_validate_schemas, filter_validate_response)


async def view(request, *args, **kwargs):
    return request.validated


def fake_request(url='/', method='GET', route='/', headers=None, body=None):
    headers = headers or {}
    headers_ = CIDict(host='127.0.0.1')
    [headers_.__setitem__(*x) for x in headers.items()]

    app = Rafter()
    app.add_route(view, route, methods=[method])

    request = app.request_class(url.encode('utf-8'), headers_,
                                '1.1', method, None)
    request.app = app
    request.body = body or b''

    return request


async def test_no_request_schema():
    get_response = filter_validate_schemas(view, {})
    rsp = await get_response(fake_request())
    assert rsp == {}


async def test_no_response_schema():
    async def view_rsp(request):
        return Response(request.validated)

    get_response = filter_validate_response(view_rsp, {})
    rsp = await get_response(fake_request())
    assert isinstance(rsp, Response)
    assert rsp.data == {}


async def test_invalid_response():
    get_response = filter_validate_response(view, {})
    with pytest.raises(TypeError) as e:
        await get_response(fake_request())

    assert str(e.value) == 'response is not an instance ' \
                           'of rafter.http.Response.'


async def test_simple_get():
    class ReqModel(Model):
        @model_node()
        class params(Model):
            p = types.IntType(required=False)

    get_response = filter_validate_schemas(view, {'request_schema': ReqModel})

    rsp = await get_response(fake_request())
    assert rsp == {'params': {'p': None}}


async def test_get_params():
    class ReqModel(Model):
        @model_node()
        class params(Model):
            p1 = types.IntType(required=True)
            p2 = types.ListType(types.IntType)

    get_response = filter_validate_schemas(view, {'request_schema': ReqModel})

    with pytest.raises(ValidationErrors) as e:
        await get_response(fake_request())

    e = e.value
    assert e.status_code == 400
    assert e.error_list == [
        {'messages': ['This field is required.'],
         'location': ['params', 'p1']}
    ]

    rsp = await get_response(fake_request('/?p1=10'))
    assert rsp == {'params': {'p1': 10, 'p2': None}}

    rsp = await get_response(fake_request('/?p1=10&p2=5'))
    assert rsp == {'params': {'p1': 10, 'p2': [5]}}

    rsp = await get_response(fake_request('/?p1=10&p2=5&p2=4'))
    assert rsp == {'params': {'p1': 10, 'p2': [5, 4]}}


async def test_headers():
    class ReqModel(Model):
        @model_node()
        class headers(Model):
            p1 = types.IntType(required=True, serialized_name='x-test')

    get_response = filter_validate_schemas(view, {'request_schema': ReqModel})

    with pytest.raises(ValidationErrors) as e:
        await get_response(fake_request())

    e = e.value
    assert e.status_code == 400
    assert e.error_list == [
        {'messages': ['This field is required.'],
         'location': ['headers', 'x-test']}
    ]

    with pytest.raises(ValidationErrors) as e:
        await get_response(fake_request(headers={'x-test': 'a'}))

    e = e.value
    assert e.status_code == 400
    assert e.error_list == [
        {'messages': ['Value \'a\' is not int.'],
         'location': ['headers', 'x-test']}
    ]

    rsp = await get_response(fake_request(headers={'x-test': '12'}))
    assert rsp == {'headers': {'x-test': 12}}


async def test_body_form():
    class ReqModel(Model):
        @model_node()
        class body(Model):
            p1 = types.IntType()
            p2 = types.ListType(types.IntType)

    get_response = filter_validate_schemas(view, {'request_schema': ReqModel})
    params = {'method': 'POST',
              'headers': {'Content-Type': 'application/x-www-form-urlencoded'}}

    rsp = await get_response(fake_request(**params))
    assert rsp == {'body': {'p1': None, 'p2': None}}

    rsp = await get_response(fake_request(body=b'p1=2&p2=5', **params))
    assert rsp == {'body': {'p1': 2, 'p2': [5]}}

    rsp = await get_response(fake_request(body=b'p1=2&p2=5', **params))
    assert rsp == {'body': {'p1': 2, 'p2': [5]}}


async def test_body_json():
    class ReqModel(Model):
        @model_node()
        class body(Model):
            p1 = types.IntType()
            p2 = types.ListType(types.IntType)

    get_response = filter_validate_schemas(view, {'request_schema': ReqModel})
    params = {'method': 'POST'}

    rsp = await get_response(fake_request(**params, body=b'{"p1": "2"}'))
    assert rsp == {'body': {'p1': 2, 'p2': None}}


async def test_response_direct():
    async def view_(request):
        return HTTPResponse('text')

    get_response = filter_validate_response(view_, {})

    rsp = await get_response(fake_request())
    assert isinstance(rsp, HTTPResponse)
    assert not isinstance(rsp, Response)
    assert rsp.body == b'text'


async def test_response_schema():
    class RspSchema(Model):
        @model_node()
        class body(Model):
            r1 = types.IntType()

    async def view_dict(request):
        return Response({'r1': 1})

    async def view_response(request):
        return Response({'r1': 2})

    async def view_error(request):
        return Response({'r1': 'abc'})

    params = {'response_schema': RspSchema}

    # With direct data return
    get_response = filter_validate_response(view_dict, params)

    rsp = await get_response(fake_request())
    assert isinstance(rsp, Response)
    assert rsp.data == {'r1': 1}

    # With Response instance return
    get_response = filter_validate_response(view_response, params)

    rsp = await get_response(fake_request())
    assert isinstance(rsp, Response)
    assert rsp.data == {'r1': 2}

    # Wrong data return
    get_response = filter_validate_response(view_error, params)

    with pytest.raises(ServerError) as e:
        await get_response(fake_request())

    e = e.value
    assert e.status_code == 500
    assert e.args == ('Wrong data output',)
