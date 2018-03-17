===============
Getting started
===============


Installation
============

Install Rafter with pip (in a virtualenv or not)::

    pip install rafter

If you'd like to test and tamper the examples, clone and install the
project::

    git clone https://github.com/olivier-m/rafter.git
    pip install -e ./rafter

You'll find the examples in the ``rafter/examples`` folder.

.. important::
    The next given command will take place in your ``rafter``
    directory.


First basic application
=======================

Our first application is super simple and only illustrates the ability to
directly return arbitrary data as a response.

.. literalinclude:: ../../examples/basic.py
    :caption: examples/basic.py
    :name: examples/basic.py

Launch this simple app with::

    python examples/basic.py

Now, in another terminal, let's call the API::

    curl http://127.0.0.1:5000/

You'll receive a response::

    {"data":"It works!"}


.. tip::
    To ease your tests, I strongly advise you to use a full-featured HTTP
    client. `Insomnia <https://insomnia.rest/>`_ is a very good one.

Now, let's see in the next part what we can do with :doc:`resources and schemas <./resources>`
