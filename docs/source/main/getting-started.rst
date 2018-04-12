===============
Getting started
===============


Installation
============

.. warning::
    Rafter works with python 3.5 or higher.

Install Rafter with pip (in a virtualenv or not)::

    pip install rafter

If you'd like to test and tamper the examples, clone and install the
project::

    git clone https://github.com/olivier-m/rafter.git
    pip install -e ./rafter


First basic application
=======================

Our first application is super simple and only illustrates the ability to
directly return arbitrary data as a response, and raise errors.

.. literalinclude:: ../../../examples/simple.py
    :caption: examples/simple.py
    :name: examples/simple.py

.. tip::
    If you cloned the repository, you'll find the examples in the :file:`rafter/examples` folder.
    The next given command will take place in your :file:`rafter` directory.

Launch this simple app with::

    python examples/simple.py

Now, in another terminal, let's call the API::

    curl http://127.0.0.1:5000/

You'll receive a response::

    {"data":"Hello there!"}

Then you can try the following API endpoints and see what it returns::

    curl http://127.0.0.1:5000/p/test-param
    curl -v http://127.0.0.1:5000/status
    curl -v http://127.0.0.1:5000/error


.. tip::
    To ease your tests, I strongly advise you to use a full-featured HTTP client. Give `Insomnia <https://insomnia.rest/>`_ a try; it's a very good client with many options.

Now, let's see in the next part what we can do with :doc:`routing and responses <./resources>`.
