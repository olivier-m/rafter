# -*- coding: utf-8 -*-
import json
import pytest

from sanic.exceptions import abort
from sanic.response import text
from rafter import Rafter, ApiError, model_node, Response

from schematics import Model, types


class SimpleHeadersModel(Model):
    foo = types.IntType(required=False, serialized_name='x-test')


class GetArgs(Model):
    @model_node()
    class params(Model):
        p1 = types.IntType(serialized_name='test', default=0)
        p2 = types.StringType(serialized_name='test_s')

    @model_node()
    class path(Model):
        tag = types.StringType(required=True)

    headers = types.ModelType(SimpleHeadersModel)


class PostArgs(Model):
    headers = types.ModelType(SimpleHeadersModel)

    @model_node()
    class body(Model):
        val1 = types.IntType(min_value=1)

    plop = types.IntType(default=1)


class OutputSchema(Model):
    name = types.StringType(required=True)
    id = types.IntType(required=True)

    @model_node()
    class extra(Model):
        op1 = types.StringType()


@pytest.yield_fixture(scope='module')
def app():
    app = Rafter()

    @app.resource('/')
    async def main(request):
        return text('main')

    @app.resource('/simple/<tag>', methods=['GET'], request_schema=GetArgs)
    async def simple_get(request, tag):
        return {
            'tag': tag,
            'res': request.validated
        }

    @app.resource('/post', methods=['POST'], request_schema=PostArgs)
    async def simple_post(request):
        return Response(request.validated, 201)

    @app.resource('/return', methods=['POST'], response_schema=OutputSchema)
    async def return_json(request):
        return request.json

    @app.resource('/error/base', methods=['GET'])
    async def error_base(request):
        raise Exception('Base 500 error')

    @app.resource('/error/sanic', methods=['GET'])
    async def error_sanic(request):
        abort(502, 'Error 502')

    @app.resource('/error/api', methods=['GET'])
    async def error_api(request):
        raise ApiError('API Error', 501, code='E001')

    yield app


@pytest.fixture(scope='function')
def test_cli(loop, app, test_client):
    return loop.run_until_complete(test_client(app))


async def test_simple(test_cli):
    res = await test_cli.get('/')
    print(await res.text())


async def test_filter_args(test_cli):
    res = await test_cli.get('/simple/tag1')
    assert await res.json() == {
        'tag': 'tag1',
        'res': {
            'params': {
                'test': 0,
                'test_s': None
            },
            'headers': {
                'x-test': None
            },
            'path': {
                'tag': 'tag1'
            }
        }
    }

    res = await test_cli.get('/simple/tag1?test=1')
    assert await res.json() == {
        'tag': 'tag1',
        'res': {
            'params': {
                'test': 1,
                'test_s': None
            },
            'headers': {
                'x-test': None
            },
            'path': {
                'tag': 'tag1'
            }
        }
    }


async def test_simple_post(test_cli):
    expected = {
        'headers': {
            'x-test': None
        },
        'body': {
            'val1': 1
        },
        'plop': 1
    }

    # With json data
    res = await test_cli.post('/post', data='{"val1": 1}')
    assert await res.json() == expected

    # With form data
    res = await test_cli.post(
        '/post', data='val1=1',
        headers={'Content-Type': 'application/x-www-form-urlencoded'})
    assert await res.json() == expected


async def test_simple_post_errors(test_cli):
    res = await test_cli.post('/post', data='{"val1": "a"}')
    assert res.status == 400
    assert await res.json() == {
        'status': 400,
        'error_list': [
            {'location': ['body', 'val1'],
             'messages': ["Value 'a' is not int."]}
        ],
        'message': 'Invalid input data'
    }


async def test_return_ok(test_cli):
    data = json.dumps({
        'id': '1',
        'name': 'Name'
    })

    res = await test_cli.post('/return', data=data)
    assert await res.json() == {
        'id': 1,
        'name': 'Name',
        'extra': {
            'op1': None
        }
    }

    data = json.dumps({
        'id': '1',
        'name': 'Name',
        'extra': {
            'op1': 12
        }
    })

    res = await test_cli.post('/return', data=data)
    assert await res.json() == {
        'id': 1,
        'name': 'Name',
        'extra': {
            'op1': '12'
        }
    }


async def test_return_ko(test_cli):
    data = json.dumps({
        'id': 'abc'
    })

    res = await test_cli.post('/return', data=data)
    assert res.status == 500
    assert await res.json() == {
        'status': 500,
        'message': 'Wrong data output'
    }


async def test_error_base(test_cli):
    res = await test_cli.get('/error/base')
    assert res.status == 500
    assert await res.json() == {
        'status': 500,
        'message': 'An error occured'
    }


async def test_error_sanic(test_cli):
    res = await test_cli.get('/error/sanic')
    assert res.status == 502
    assert await res.json() == {
        'status': 502,
        'message': 'Error 502'
    }


async def test_error_api(test_cli):
    res = await test_cli.get('/error/api')
    assert res.status == 501
    assert await res.json() == {
        'status': 501,
        'code': 'E001',
        'message': 'API Error'
    }
