==========================
Filters and Error Handlers
==========================

Filters
=======

Filters are like middlewares but applied to a specific resource. They have an API similar to what Django offers.

Here's a basic prototype of a filter:

.. code-block:: python

    def basic_filter(get_response, params):
        # get_response is the view function or the next filter on the chain
        # params are the resource parameters

        # This part is called during the resource initialization.
        # You can configure, for instance, things based on params values.

        async def decorated_filter(request, *args, **kwargs):
            # Pre-Response code. You can change request attributes,
            # raise exceptions, call another response function...

            # Processing resource (view)
            result = await get_response(request, *args, **kwargs)

            # Post-Response code. You can change the response attributes,
            # raise exceptions, log things...

        # Don't forget this!
        return decorated_filter


A filter is a decorator function. It must return an asynchronous callable that will handle the request and will return a response or the result of the ``get_response`` function.

On Rafter' side, you can pass the `` filters`` or the ``validators`` parameter (both lists) to :meth:`rafter.app.Rafter.resource`.

Each filter will then be chained to the other, in their order of declaration.

.. important::
    The ``Rafter`` class has one default validator: ``filter_transform_response`` that transforms the response when possible.

    If you pass the ``filters`` argument to your resource, you'll override the default filters. If that's not what you want, you can pass the ``validators`` argument instead. These filters will then be chained to the default filters.

.. seealso::
    - :meth:`rafter.app.Rafter.resource`
    - :func:`rafter.filters.filter_transform_response`


Example
-------

The following example demonstrates two filters. The first one changes the response according to the value of ``?action`` in the query string. The second serializes data to plist format when applicable.

.. literalinclude:: ../../../examples/filters.py
    :caption: examples/filters.py
    :name: examples/filters.py


Error Handlers
==============

Rafter provides 3 default error handlers and one exception class :class:`rafter.exceptions.ApiError`.

All 3 handlers return a structured JSON response containing at least a ``message`` and a ``status``. If the Rafter app is in debuging mode, they also return a structured stack trace.

Here are the exception classes handled by the default error handlers:

:class:`rafter.exceptions.ApiError`:
    This exception's message, status and extra argument are returned.

:class:`sanic.exceptions.SanicException`:
    This exception's message and status are returned

:class:`Exception`:
    For any other exception, a fixed error with status **500** and **An error occured.** message.


.. seealso::
    - :mod:`rafter.exceptions`
    - :attr:`rafter.app.Rafter.default_error_handlers`


Example
-------

.. literalinclude:: ../../../examples/errors.py
    :caption: examples/errors.py
    :name: examples/errors.py
