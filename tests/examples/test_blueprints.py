# -*- coding: utf-8 -*-
from examples.blueprints import app


def test_main_view():
    request, response = app.test_client.get('/')
    assert response.status == 404


def test_v1_main():
    request, response = app.test_client.get('/v1/')
    assert response.status == 200
    assert response.json == {'version': 1}
    assert 'abc' not in response.headers


def test_v1_test():
    request, response = app.test_client.get('/v1/test')
    assert response.status == 200
    assert response.json == [3, 2, 1]


def test_v2_main():
    request, response = app.test_client.get('/v2/')
    assert response.status == 200
    assert response.json == {'version': 2}
    assert response.headers['x-test'] == 'abc'
