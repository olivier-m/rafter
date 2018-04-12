# -*- coding: utf-8 -*-
from examples.basic import app


def test_main_view():
    request, response = app.test_client.get('/')
    assert response.status == 200
    assert response.json == {'data': 'It works!'}
