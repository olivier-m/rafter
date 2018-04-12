# -*- coding: utf-8 -*-
from examples.simple import app


def test_main_view():
    request, response = app.test_client.get('/')
    assert response.status == 200
    assert response.json == {'data': 'Hello there!'}


def test_with_params():
    request, response = app.test_client.get('/p/test-param')
    assert response.status == 200
    assert response.json == ['test-param']


def test_status():
    request, response = app.test_client.get('/status')
    assert response.status == 201
    assert response.json == {'test': 'abc'}


def test_error():
    request, response = app.test_client.get('/error')
    assert response.status == 501
    assert response.json == {'status': 501,
                             'message': 'Something bad happened!',
                             'extra_data': ':('}
