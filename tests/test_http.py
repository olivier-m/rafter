# -*- coding: utf-8 -*-

from sanic.response import HTTPResponse

from rafter.http import Request, Response


def test_request():
    r = Request(b'', '', 1, 'GET', 'http')
    assert r.validated == {}


def test_response():
    r = Response({'test': 1})
    rsp = r.response()

    assert isinstance(rsp, HTTPResponse)
    assert rsp.status == 200
    assert rsp.headers == {}
    assert rsp.content_type == 'application/json'
    assert rsp.body == b'{"test":1}'

    r = Response({'test': 2}, 201, {'x-test': 'test'})
    rsp = r.response()

    assert isinstance(rsp, HTTPResponse)
    assert rsp.status == 201
    assert rsp.headers == {'x-test': 'test'}
    assert rsp.content_type == 'application/json'
    assert rsp.body == b'{"test":2}'
