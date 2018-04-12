# -*- coding: utf-8 -*-
from examples.contrib_schematics import app


def test_main_view():
    request, response = app.test_client.get('/')
    assert response.status == 200
    assert response.text == 'Hi mate!'


def test_post_json_ok():
    data = {
        'id': 2,
        'extra-data': 'ignored data'
    }
    headers = {
        'x-test': '5'
    }

    request, response = app.test_client.post('/post', json=data,
                                             headers=headers)
    assert response.status == 201
    assert response.json['raw'] == data
    assert response.json['validated'] == request.validated
    assert request.validated == {
        'body': {
            'id': 2,
            'name': ''
        },
        'headers': {
            'x-test': 5
        }
    }

    data['name'] = 'olivier'

    request, response = app.test_client.post('/post', json=data,
                                             headers=headers)
    assert response.status == 201
    assert response.json['raw'] == data
    assert response.json['validated'] == request.validated
    assert request.validated == {
        'body': {
            'id': 2,
            'name': 'olivier'
        },
        'headers': {
            'x-test': 5
        }
    }


def test_post_json_errors():
    request, response = app.test_client.post('/post', json={})
    assert response.status == 400
    assert response.json == {
        'error_list': [{'location': ['body', 'id'],
                        'messages': ['This field is required.']}],
        'message': 'Invalid input data',
        'status': 400
    }
    assert request.validated == {}

    request, response = app.test_client.post('/post', json={'id': 'abc'},
                                             headers={'x-test': 'xyz'})
    assert response.status == 400
    assert response.json == {
        'error_list': [{'location': ['body', 'id'],
                        'messages': ["Value 'abc' is not int."]},
                       {'location': ['headers', 'x-test'],
                        'messages': ["Value 'xyz' is not int."]}],
        'message': 'Invalid input data',
        'status': 400
    }


def test_post_form_ok():
    headers = {
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = 'id=1&name=olivier'

    request, response = app.test_client.post('/post', data=data,
                                             headers=headers)

    assert response.status == 201
    assert response.json['raw'] == {'id': ['1'], 'name': ['olivier']}
    assert response.json['validated'] == request.validated
    assert request.validated == {
        'body': {
            'id': 1,
            'name': 'olivier'
        },
        'headers': {
            'x-test': 0
        }
    }


def test_get_tags_ok():
    request, response = app.test_client.get('/tags/xyz')
    assert response.status == 200
    assert response.json == {
        'args': {},
        'tag': 'xyz',
        'validated': {'params': {'page': 1, 'sort': 'asc'},
                      'path': {'tag': 'xyz'}}
    }

    request, response = app.test_client.get('/tags/abc?page=2&sort=desc')
    assert response.status == 200
    assert response.json == {
        'args': {'page': ['2'], 'sort': ['desc']},
        'tag': 'abc',
        'validated': {'params': {'page': 2, 'sort': 'desc'},
                      'path': {'tag': 'abc'}}
    }


def test_get_tags_ko():
    request, response = app.test_client.get('/tags/abc12?sort=z&page=-4')
    assert response.status == 400
    assert response.json == {
        'error_list': [{'location': ['params', 'page'],
                        'messages': ['Int value should be greater than or '
                                     'equal to 1.']},
                       {'location': ['params', 'sort'],
                        'messages': ["Value must be one of ('asc', 'desc')."]},
                       {'location': ['path', 'tag'],
                        'messages': ['String value did not match '
                                     'validation regex.']}],
        'message': 'Invalid input data',
        'status': 400}


def test_return_ok():
    data = {
        'name': 'olivier'
    }

    request, response = app.test_client.post('/return', json=data)
    assert response.status == 200
    assert response.json == {'name': 'olivier', 'options': {'xray': False}}
    assert response.headers['x-response'] == '5'

    data['options'] = {'xray': '1'}
    request, response = app.test_client.post('/return', json=data)
    assert response.status == 200
    assert response.json == {'name': 'olivier', 'options': {'xray': True}}


def test_return_ko():
    request, response = app.test_client.post('/return', json={})
    assert response.status == 500
    assert response.json == {'message': 'Wrong data output', 'status': 500}
