# -*- coding: utf-8 -*-
import plistlib

from examples.filters import app


def test_input():
    request, response = app.test_client.get('/input')
    assert response.status == 200
    assert response.json == {}

    request, response = app.test_client.get('/input?action=text')
    assert response.status == 200
    assert response.content_type == 'text/plain'
    assert response.body == b'test response'

    request, response = app.test_client.get('/input?action=abort')
    assert response.status == 500
    assert response.json == {'status': 500, 'message': 'Abort!'}


def test_output():
    data = {'a': 1, 'b': ['x', 'y', 'z']}

    request, response = app.test_client.post('/output', json=data)
    assert response.status == 200
    assert response.content_type == 'application/json'
    assert response.json == data

    request, response = app.test_client.post(
        '/output', json=data, headers={'accept': 'application/plist+xml'})
    assert response.content_type == 'application/plist+xml'
    assert plistlib.loads(response.body) == data
