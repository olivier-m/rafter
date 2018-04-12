# -*- coding: utf-8 -*-
from sanic.response import HTTPResponse

from rafter.app import Rafter
from rafter.http import Response
from rafter.filters import filter_transform_response


def fake_request():
    app = Rafter()

    request = app.request_class(b'/', {}, '1.1', 'GET', None)
    request.app = app
    request.body = b''

    return request


async def test_data_response():
    async def view_base(request):
        return {'a': 1}

    get_response = filter_transform_response(view_base, {})
    res = await get_response(fake_request())
    assert isinstance(res, Response)
    assert res.data == {'a': 1}


async def test_rafter_response():
    async def view_base(request):
        return Response({'a': 1})

    get_response = filter_transform_response(view_base, {})
    res = await get_response(fake_request())
    assert isinstance(res, Response)
    assert res.data == {'a': 1}


async def test_sanic_response():
    async def view_base(request):
        return HTTPResponse('abc')

    get_response = filter_transform_response(view_base, {})
    res = await get_response(fake_request())
    assert not isinstance(res, Response)
    assert res.body == b'abc'
