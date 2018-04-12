# -*- coding: utf-8 -*-
from examples.errors import app


def test_main_view():
    request, response = app.test_client.get('/')
    assert response.status == 500
    assert response.json == {'status': 500,
                             'message': 'An error occured.'}


def test_api_error():
    request, response = app.test_client.get('/api')
    assert response.status == 599
    assert response.json == {'status': 599,
                             'message': 'Something went very wrong.',
                             'explanation': 'http://example.net/',
                             'xtra': 12}


def test_sanic_error():
    request, response = app.test_client.get('/sanic')
    assert response.status == 599
    assert response.json == {'status': 599,
                             'message': 'A bad error.'}
