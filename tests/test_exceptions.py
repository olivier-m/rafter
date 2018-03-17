# -*- coding: utf-8 -*-

from rafter.exceptions import ApiError, ValidationErrors


def test_apierror():
    e = ApiError('error')
    assert e.status_code == 500
    assert e.data == {}

    e = ApiError('error', 400, xtra=1)
    assert e.status_code == 400
    assert e.data == {'xtra': 1}
    assert e.to_primitive() == e.data


def test_validationerror():
    errors = {
        'body': {
            'age': ['invalid age'],
            'name': ['invalid name'],
            'options': {
                'op1': ['invalid option'],
                'extra': {
                    'ex1': ['invalid ex1'],
                    'ex2': ['invalid ex2']
                }
            }
        }
    }

    e = ValidationErrors(errors, xtra='message')
    assert e.status_code == 400

    error_list = e.error_list
    assert error_list == [
        {'messages': ['invalid age'],
         'location': ['body', 'age']},
        {'messages': ['invalid name'],
         'location': ['body', 'name']},
        {'messages': ['invalid ex1'],
         'location': ['body', 'options', 'extra', 'ex1']},
        {'messages': ['invalid ex2'],
         'location': ['body', 'options', 'extra', 'ex2']},
        {'messages': ['invalid option'],
         'location': ['body', 'options', 'op1']}
    ]

    assert e.to_primitive() == {'xtra': 'message',
                                'error_list': error_list}
