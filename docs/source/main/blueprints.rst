==========
Blueprints
==========

Rafter provides a blueprint API similar to what Sanic provides. The :class:`rafter.blueprints.Blueprint` adds two methods to register resources:

- ``resource``
- ``add_resource``

You must use :class:`rafter.blueprints.Blueprint` if you plan to add resources to your blueprint.

.. seealso::
    - :mod:`rafter.blueprints`


Example
=======

.. literalinclude:: ../../../examples/blueprints.py
    :caption: examples/blueprints.py
    :name: examples/blueprints.py
