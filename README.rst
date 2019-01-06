=================
Django-dataporten
=================

Django-dataporten is a simple Django app to fetch data from dataporten and connect it to a user.

Quick start
-----------

1. Add "dataporten" to your INSTALLED_APPS setting like this

.. code:: python

    INSTALLED_APPS = [
        ...
        'dataporten',
    ]


2. Run `python manage.py migrate` to create the dataporten proxy models.

3. In your settings.py file, add the variable DATAPORTEN_TOKEN_FUNCTION, which should be a dotted path to the function that will retrieve user tokens. The function should accept a :code:`User` and return a :code:`str`. Here is a python3.6 example that will work if you use `django-allauth`_:

.. code:: python

    def allauth_token(user: User) -> str:
        return SocialToken.objects.get(
            account__user=user,
            account__provider='dataporten',
        ).token

.. _django-allauth: https://github.com/pennersr/django-allauth:

Run tests
_________

.. code:: bash

    export DJANGO_SETTINGS_MODULE=dataporten.settings
    pytest
