=================================
Resources, schemas and validation
=================================


Resource routes
===============

Routing a resource with Rafter is the same thing as adding a route in Sanic except that we do it with the ``resource`` decorator of the Rafter App instance.

In this example, ``app`` is an instance of the ``Rafter`` class.

.. code-block:: python
    :emphasize-lines: 1

    @app.resource('/)
    async def test(request):
        return {'hello': 'world'}

The ``resource`` decorator takes the same arguments as Sanic ``route``, plus a few ones that we're going to explore.

.. seealso::
    :class:`rafter.app.Rafter`


Schemas
=======

But first, we'll need to see how to create and, later, declare schema for our input and output data.

Schemas with Rafter are made using `Schematic <schematics_>`_. So, let's make a simple schema.

.. code-block:: python

    from schematics import Model, types

    class BodySchema(Model):
        name = types.StringType(required=True)

    class InputSchema(Model):
        body = types.ModelType(BodySchema)

In this example, ``InputSchema`` declares a ``body`` property that is another schema. Now, let's use it in our view:

.. code-block:: python
    :emphasize-lines: 2,4

    @app.resource('/', ['POST'],
                  request_schema=InputSchema)
    async def test(request):
        return request.validated

If the input data is not valid, the request to this route will end up with an HTTP error 400 returning a structured error. If everything went well, you can access your processed data with ``request.validated``.

Let's say now that we want to return the input body that we received and use a schema to validate the output data. Here's how to do it:

.. code-block:: python
    :emphasize-lines: 3

    @app.resource('/', ['POST'],
                  request_schema=InputSchema,
                  response_schema=BodySchema)
    async def test(request):
        return {}

In that case, the ``response_schema`` will fail because ``name`` is a required field. It will end up with an HTTP error 500.


The model_node decorator
========================

Having to create many classes and use the ``types.ModelType`` could be annoying, although convenient at time. Rafter offers a decorator to directly instantiate a sub-node in your schema. Here's how it applies to our ``InputSchema``:

.. code-block:: python
    :emphasize-lines: 5

    from schematics import Model, types
    from rafter import model_node

    class InputSchema(Model):
        @model_node()
        class body(Model):
            name = types.StringType(required=True)

.. seealso::
    :func:`rafter.schema.model_node`


.. _rafter_request_schema:

Request (input) schema
======================

An request schema is set with the ``request_schema`` of your resource. It must be a Schematics Model instance with the following, optional, sub schemas:

- ``body``: Used to validate your request's body data (form url encoded or json)
- ``params``: To validate your URL arguments
- ``path``: To validate data in the path parameters
- ``headers``: To validate request headers


.. _rafter_response_schema:

Response (output) schema
========================

A response schema is a normal Schematics Model instance and will be validated by the response filter when necessary.

.. important::
        The response validation is only effective when:

        - A ``response_schema`` has been provided by the resource definition
        - The resource returns a :ref:`rafter_response` instance
          or arbitrary data.


.. _rafter_response:

rafter.http.Response
====================

The Rafter ``Response`` is a specialized Sanic ``HTTPResponse``. It acts almost in the same way except that it takes arbitrary data as input and serializes the response's body at the very last moment.

You can use it to return a special status:

.. code-block:: python
    :emphasize-lines: 5

    from rafter import Response

    @app.resource('/)
    async def test(request):
        return Response({'hello': 'world'}, 201)

.. note::
    When you return arbitrary data from a resource, you actually return a Rafter ``Response`` instance, so validation also works in that case.

.. seealso::
    :class:`rafter.http.Response`


Filters and validators
======================

Filters are like middlewares but applied to a specific resource. They have an api similar to what Django offers.

Here's a simple filter example:

.. code-block:: python
    :emphasize-lines: 17

    from sanic.exceptions import abort
    from sanic.response import text

    def basic_filter(get_response, params):
        async def decorated_filter(request, *args, **kwargs):
            if request.args.get('action') == 'abort':
                abort(500, 'Abort!')

            if request.args.get('action') == 'text':
                return text('test response')

            return await get_response(request, *args, **kwargs)

        return decorated_filter

    @app.resource('/filter',
                  validators=[basic_filter])
    async def filtered(request):
        return request.args

A filter must return an async callable that will handle the request and must return a response or the result of the ``get_response`` function.

Filters and validators are chained and called in the order of declaration.

.. important::
    The ``Rafter`` class has two default validators:

    - ``filter_validate_schemas``: Validate the request data if a request schema it set.
    - ``filter_validate_response``: Prepare the response and validate it if a response schema is set.

    If you pass the ``filters`` argument to your resource, you'll override the default filters. If that's not what you want, you can pass the ``validators`` argument instead. These filters will then be chained to the default filters.

.. seealso::
    - :func:`rafter.filters.filter_validate_schemas`
    - :func:`rafter.filters.filter_validate_response`



Error management
================

Any ``Exception`` based error raised by your routes will be caught by the default ``error_handler`` and returned in a structured, predictable dict.

.. literalinclude:: ../../examples/errors.py
    :caption: examples/errors.py
    :name: examples/errors.py

.. seealso::
    :ref:`rafter_exceptions`


Now you can dig to a :doc:`full example <./example>` or explore the :doc:`API reference <./reference>`.
