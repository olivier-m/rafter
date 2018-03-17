# -*- coding: utf-8 -*-
from schematics import types

__all__ = ('model_node',)


def model_node(**kwargs):
    """
    Decorates a ``schematics.Model`` class to add it as a field
    of type ``schematic.types.ModelType``.

    Keyword arguments are passed to ``schematic.types.ModelType``.

    Example:

    .. code-block:: python
        :emphasize-lines: 6,11

        from schematics import Model, types

        class MyModel(Model):
            name = types.StringType()

            @model_node()
            class options(Model):
                status = types.IntType()

            # With arguments and another name
            @model_node(serialized_name='extra', required=True)
            class _extra(Model):
                test = types.StringType()
    """
    kwargs.setdefault('default', {})

    def decorator(model):
        return types.ModelType(model, **kwargs)

    return decorator
