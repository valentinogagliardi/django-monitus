===================
django-monitus
===================

.. image:: https://img.shields.io/twitter/follow/gagliardi_vale?style=social
   :target: https://twitter.com/gagliardi_vale

.. image:: https://github.com/valentinogagliardi/django-monitus/workflows/Test%20suite/badge.svg
   :target: https://github.com/valentinogagliardi/django-monitus/actions

Tiny error reporting middleware(s) for Django.

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

Setup either ``ADMINS`` or ``MANAGERS`` in your settings:

.. code-block:: python
    MANAGERS = [("Juliana C.", "juliana.crain@dev.io")]
