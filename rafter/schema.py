# -*- coding: utf-8 -*-
from schematics import types

__all__ = ('model_node',)


def model_node(**kwargs):
    kwargs.setdefault('default', {})

    def decorator(model):
        return types.ModelType(model, **kwargs)

    return decorator
