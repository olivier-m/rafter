======
Rafter
======

Overview
========

Rafter is a Python 3.5+ library providing building blocks for Restfull APIs. Yes, it's yet another framework trying, again, to solve the same problem!

Rafter is built on top of `Sanic <sanic_>`_, an asynchronous and blazingly fast HTTP Python framework.


Not solving every problem
=========================

A Restfull framework tries to solve specific problems with the unwritten protocol that is REST and Rafter is no exception. However, its main goals are to **provide a good user interface** (the Python API) and to **solve as few problems as possible**.

A solid API is key; it must be consistent, clear, easy to learn and use. Rafter kits you with a few classes and functions to help you create a great API but will do its best to get out of your way and let you do what needs to be done.
You (the developer) should have fun coding whatever project you're coding instead of fighting and twisting your framework.

That said, Rafter provides some facilities to handle the very common use cases that come with writing a Restfull API:

- Declare your resources,
- Provide filtering and transformation routines,
- Handle errors with clear, extendible, structured data.

And that's it! The rest is up to you; bring your ideas, your favourite ORM, write your own filters. Have fun!


Example
=======

.. literalinclude:: ../../examples/basic.py

Now, let's see more examples and usage instruction in :doc:`the next part <./main/getting-started>`.


.. toctree::
    :maxdepth: 2
    :caption: Contents

    main/getting-started
    main/resources
    main/filters-and-errors
    main/blueprints

    contrib/schematics/index

    api/index


All examples
============

* :any:`Simple first API <examples/simple.py>`
* :any:`Error handlers <examples/errors.py>`
* :any:`Request and response filters <examples/filters.py>`
* :any:`Blueprints <examples/blueprints.py>`
* :any:`Schema validation with Schematics <examples/contrib_schematics.py>`


Contribute!
===========

* `Source Code <https://github.com/olivier-m/rafter/>`__
* `Bug reports <https://github.com/olivier-m/rafter/issues>`__


Miscellaneous links
===================

* :ref:`genindex`
* :ref:`modindex`
