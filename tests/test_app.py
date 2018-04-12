# -*- coding: utf-8 -*-
import pytest

from sanic.response import text

from rafter import Rafter
from rafter.http import Request


def test_app():
    Rafter(name='abc')

    # No positional arguments
    with pytest.raises(TypeError):
        Rafter('name')


def test_app_request_class():
    class Req(Request):
        pass

    Rafter(request_class=Req)

    class Req2(object):
        pass

    with pytest.raises(RuntimeError):
        Rafter(request_class=Req2)


def test_app_resource():
    app = Rafter()

    @app.resource('/')
    def test(request):
        pass

    @app.resource('/strm', stream=True)
    def strm(request):
        pass

    route = app.router._get('/strm', 'GET', '')
    assert route[0].is_stream is True


def test_app_filters():
    def filter1(get_response, params):
        async def func(request, *args, **kwargs):
            return await get_response(request, *args, **kwargs)

        return func

    def filter2(get_response, params):
        async def func(request, *args, **kwargs):
            resp = await get_response(request, *args, **kwargs)
            return text(resp.body.decode('utf-8') + 'xyz')

        return func

    app = Rafter()

    @app.resource('/', filters=[filter1])
    async def test(request):
        return text('abc')

    @app.resource('/tr', filters=[filter1, filter2])
    async def testTR(request):
        return text('abc')

    request, response = app.test_client.get('/')
    assert response.status == 200
    assert response.body == b'abc'

    request, response = app.test_client.get('/tr')
    assert response.status == 200
    assert response.body == b'abcxyz'
