=============
API Reference
=============

rafter.app
==========

.. autoclass:: rafter.app.Rafter

    .. autoattribute:: default_filters
    .. autoattribute:: default_error_handlers
    .. autoattribute:: default_request_class

    .. automethod:: add_resource
    .. automethod:: resource


rafter.http
===========

.. autoclass:: rafter.http.Request

.. autoclass:: rafter.http.Response


rafter.schema
=============

.. autofunction:: rafter.schema.model_node


.. _rafter_exceptions:

rafter.exceptions
=================

Exceptions
----------

.. autoexception:: rafter.exceptions.ApiError

    .. autoattribute:: data
    .. automethod:: to_primitive

.. autoexception:: rafter.exceptions.ValidationErrors

    .. autoattribute:: data
    .. autoattribute:: error_list

Error Handlers
--------------

.. autoclass:: rafter.exceptions.ExceptionHandler

    .. automethod:: __call__

.. autoclass:: rafter.exceptions.SanicExceptionHandler

.. autoclass:: rafter.exceptions.ApiErrorHandler


rafter.filters
==============

See :ref:`rafter_request_schema` and :ref:`rafter_response_schema` for schema definitions.

.. autofunction:: rafter.filters.filter_validate_schemas
.. autofunction:: rafter.filters.filter_validate_response
