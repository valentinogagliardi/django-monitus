===================
django-monitus
===================

.. image:: https://img.shields.io/twitter/follow/gagliardi_vale?style=social
   :target: https://twitter.com/gagliardi_vale

.. image:: https://github.com/valentinogagliardi/django-monitus/workflows/Tox%20tests/badge.svg
   :target: https://github.com/valentinogagliardi/django-monitus/actions

Tiny error reporting middleware(s) for Django. Includes the following middlewares:

- ``Error403EmailsMiddleware``: sends an email to ``ADMINS`` on 403.
- ``FailedLoginMiddleware``: sends an email to ``ADMINS`` on failed logins.

Requirements
------------

Tested on Python 3.8.

Tested on Django 3.0 and 3.1.

Setup
------------
Install from pip:

.. code-block:: sh

    python -m pip install django-monitus

Then add it to the list of installed apps:

.. code-block:: python

    INSTALLED_APPS = [
    ...
    "monitus"
    ...
    ]

Enable the desired middleware:

.. code-block:: python

    MIDDLEWARE = [
    ...
    "monitus.middleware.Error403EmailsMiddleware"
    ...
    ]

Setup ``ADMINS`` in your settings:

.. code-block:: python

    MANAGERS = [("Juliana C.", "juliana.crain@dev.io")]

Usage with asynchronous Django
------------------------------

As of now only ``Error403EmailsMiddleware`` can run asynchronously under ASGI. If you plan to use ``FailedLoginMiddleware`` and ``Error403EmailsMiddleware`` together make sure to place ``Error403EmailsMiddleware`` **before** (reading top to bottom) ``FailedLoginMiddleware``:

.. code-block:: python

    MIDDLEWARE = [
    "monitus.middleware.FailedLoginMiddleware",
    "monitus.middleware.Error403EmailsMiddleware" # this should go before FailedLoginMiddleware
    ...
    ]

This way the async chain doesn't get broken when the response traverses the middleware chain to exit out to the user.

Development and testing
-----------------------

To test on your local machine with Postgres, make sure to have a role with enough privileges:

.. code-block:: bash

    CREATE ROLE monitustestuser WITH LOGIN PASSWORD 'monitustestpassword' CREATEDB;

Then run

.. code-block:: bash

    DATABASE_URL=postgres://monitustestuser:monitustestpassword@localhost/monitustestdb tox