# -*- coding: utf-8 -*-
import json
import logging

from sanic.exceptions import abort, SanicException
from sanic.response import HTTPResponse
from sanic.server import CIDict

from rafter.app import Rafter
from rafter.exceptions import (
    ApiError,
    ExceptionHandler, SanicExceptionHandler, ApiErrorHandler)


def view(request):
    return b''


def fake_request():
    headers = CIDict(host='127.0.0.1')

    app = Rafter()
    app.add_route(view, '/', methods=['GET'])

    request = app.request_class(b'/', headers, '1.1', 'GET', None)
    request.app = app

    return request


def test_apierror():
    e = ApiError('error')
    assert e.status_code == 500
    assert e.data == {}

    e = ApiError('error', 400, xtra=1)
    assert e.status_code == 400
    assert e.data == {'xtra': 1}
    assert e.to_primitive() == e.data


def test_exception_handler(caplog):
    caplog.set_level(logging.ERROR)
    req = fake_request()

    res = ExceptionHandler()(req, ApiError('error message', 510))
    assert isinstance(res, HTTPResponse)
    assert res.status == 500
    assert json.loads(res.body.decode('utf-8')) == {
        'status': 500,
        'message': 'An error occured.'
    }
    assert caplog.record_tuples == [
        ('rafter.exceptions', logging.ERROR, 'error message')]

    caplog.clear()
    req.app.debug = True
    res = ExceptionHandler()(req, Exception('this is bad'))
    assert res.status == 500
    assert json.loads(res.body.decode('utf-8')) == {
        'status': 500,
        'message': 'An error occured.',
        'stack': []
    }
    assert caplog.record_tuples == [
        ('rafter.exceptions', logging.ERROR, 'this is bad')]


def test_sanic_exception_handler():
    res = SanicExceptionHandler()(fake_request(),
                                  SanicException('error message', 510))
    assert res.status == 510
    assert json.loads(res.body.decode('utf-8')) == {
        'status': 510,
        'message': 'error message'
    }


def test_api_error_handler():
    res = ApiErrorHandler()(fake_request(),
                            ApiError('not found', 404, xtra='abc'))
    assert res.status == 404
    assert json.loads(res.body.decode('utf-8')) == {
        'status': 404,
        'message': 'not found',
        'xtra': 'abc'
    }


def test_default_error_handlers():
    app = Rafter()

    @app.resource('/exc')
    def exc(request):
        raise ValueError('Some error')

    @app.resource('/sanicerror')
    def sanicerror(request):
        abort(409, 'conflicting')

    @app.resource('/apierror')
    def apierror(request):
        raise ApiError('could not find', 404, xtra='xyz')

    request, response = app.test_client.get('/exc')
    assert response.status == 500
    assert response.json == {'status': 500, 'message': 'An error occured.'}

    request, response = app.test_client.get('/sanicerror')
    assert response.status == 409
    assert response.json == {'status': 409, 'message': 'conflicting'}

    request, response = app.test_client.get('/apierror')
    assert response.status == 404
    assert response.json == {'status': 404,
                             'message': 'could not find',
                             'xtra': 'xyz'}
