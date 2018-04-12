=======================
Resources and Responses
=======================


Resource routes
===============

Routing a resource with Rafter is the same thing as adding a route in Sanic except that we do it with the ``resource`` decorator of the Rafter App instance.

In this example, ``app`` is an instance of the ``Rafter`` class.

.. code-block:: python
    :emphasize-lines: 1

    @app.resource('/)
    async def test(request):
        return {'hello': 'world'}

The ``resource`` decorator takes the same arguments as Sanic ``route`` and, some extra arguments that are used by :doc:`filters <./filters-and-errors>`.

.. seealso::
    :class:`rafter.app.Rafter`


.. _rafter_response:

rafter.http.Response
====================

The Rafter ``Response`` is a specialized Sanic ``HTTPResponse``. It acts almost in the same way except that it takes arbitrary data as input and serializes the response's body at the very last moment.

You can use it to return a specific status code:

.. code-block:: python
    :emphasize-lines: 5

    from rafter import Response

    @app.resource('/)
    async def test(request):
        return Response({'hello': 'world'}, 201)

.. note::
    When you return arbitrary data from a resource, Rafter will convert it to a ``Response`` instance.

.. seealso::
    :class:`rafter.http.Response`

