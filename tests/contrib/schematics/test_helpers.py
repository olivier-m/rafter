# -*- coding: utf-8 -*-
from schematics import Model, types

from rafter.contrib.schematics import model_node


def test_model_node_decorator():
    class Args(Model):
        @model_node()
        class params(Model):
            t1 = types.IntType()

        @model_node(serialized_name='test_node')
        class foo(Model):
            p1 = types.StringType()

        p = types.IntType()

    data = {
        'params': {
            't1': 1
        },
        'test_node': {
            'p1': 'test'
        },
        'p': 2,
        'extra': 'ignored'
    }

    m = Args(data, lazy=True, validate=False)
    m.validate()
    assert m.to_native() == {
        'params': {
            't1': 1
        },
        'test_node': {
            'p1': 'test'
        },
        'p': 2
    }
