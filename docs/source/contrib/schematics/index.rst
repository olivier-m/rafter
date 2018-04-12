=================================
Schema validation with Schematics
=================================

To perform schema validation using `Schematic <schematics_>`_, you need to use the ``RafterSchematics`` class instead of the ``Rafter`` one we've seen so far.

.. code-block:: python

    from rafter.contrib.schematics import RafterSchematics

    app = RafterSchematics()

This Rafter class adds two new parameters to the **resource** decorator:

- ``request_schema``: The request data validation schema
- ``response_schema``: The response validation schema

.. seealso::
    For more information on the RafterSchematics class and new filters being used, see the :mod:`rafter.contrib.schematics.app` module.


Schemas
=======

Request and response schemas are made using `Schematic <schematics_>`_. Let's start with a simple schema:

.. code-block:: python

    from schematics import Model, types

    class BodySchema(Model):
        name = types.StringType(required=True)

    class InputSchema(Model):
        body = types.ModelType(BodySchema)

In this example, ``InputSchema`` declares a ``body`` property that is another schema. Now, let's use it in our view:

.. code-block:: python
    :emphasize-lines: 4,6

    app = RafterSchematics()

    @app.resource('/', ['POST'],
                  request_schema=InputSchema)
    async def test(request):
        return request.validated

If the input data is not valid, the request to this route will end up with an HTTP 400 error returning a structured error. If everything went well, you can access your processed data with ``request.validated``.

Let's say now that we want to return the input body that we received and use a schema to validate the output data. Here's how to do it:

.. code-block:: python
    :emphasize-lines: 5

    app = RafterSchematics()

    @app.resource('/', ['POST'],
                  request_schema=InputSchema,
                  response_schema=InputSchema)
    async def test(request):
        return {}

In that case, the ``response_schema`` will fail because ``name`` is a required field. It will end up with an HTTP 500 error.


The model_node decorator
========================

Having to create many classes and use the ``types.ModelType`` could be annoying, although convenient at time. Rafter offers a decorator to directly instantiate a sub-node in your schema. Here's how it applies to our ``InputSchema``:

.. code-block:: python
    :emphasize-lines: 5

    from schematics import Model, types
    from rafter.contrib.schematics import model_node

    class InputSchema(Model):
        @model_node()
        class body(Model):
            name = types.StringType(required=True)

.. seealso::
    :func:`rafter.contrib.schematics.helpers.model_node`


.. _schematics_request_schema:

Request (input) schema
======================

An request schema is set with the ``request_schema`` parameter of your resource. It must be a Schematics Model instance with the following, optional, sub schemas:

- ``body``: Used to validate your request's body data (form url-encoded or json)
- ``params``: To validate the query string parameters
- ``path``: To validate data in the path parameters
- ``headers``: To validate the request headers


.. _schematics_response_schema:

Response (output) schema
========================

A response schema is set with the ``response_schema`` parameter of your resource. It must be a Schematics Model instance with the following, optional, sub schemas:

- ``body``: Used to validate your response body data
- ``headers``: To validate the response headers

.. important::
        The response validation is only effective when:

        - A ``response_schema`` has been provided by the resource definition
        - The resource returns a :ref:`rafter_response` instance
          or arbitrary data.


Example
=======

.. literalinclude:: ../../../../examples/contrib_schematics.py
    :caption: examples/contrib_schematics.py
    :name: examples/contrib_schematics.py
