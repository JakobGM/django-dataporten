=================
Django-dataporten
=================

Django-dataporten is a simple Django app to fetch data from dataporten and
connect it to a user.

Setup
-----

1. Add "dataporten" to your INSTALLED_APPS setting like this

.. code:: python

    INSTALLED_APPS = [
        ...
        'dataporten',
    ]


2. Run `python manage.py migrate` to create the dataporten proxy models.

3. In your settings.py file, add the variable DATAPORTEN_TOKEN_FUNCTION, which
should be a dotted path to the function that will retrieve user tokens.
The function should accept a :code:`User` and return a :code:`str`.
Here is a python3.6/3.7 example that will work if you use `django-allauth`_:

.. code:: python

    def allauth_token(user: User) -> str:
        return SocialToken.objects.get(
            account__user=user,
            account__provider='dataporten',
        ).token

4. Add the dataporten middleware. This middleware adds a :code:`dataporten`
attribute to :code:`request.user` for users with an associated
dataporten :code:`SocialToken` object. Take care to place it after
:code:`django.contrib.auth.middleware.AuthenticationMiddleware`.

.. code:: python

    MIDDLEWARE = (
        # Other middleware...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        # Other middleware...

        # Adds dataporten API information to request.user.dataporten
        # Needs to be placed after any authentication middleware, as this
        # requires inspection of request.user
        'dataporten.middleware.DataportenGroupsMiddleware',
        # Other middleware...
    )

5. Optionally, enable caching for API queries. Take care to create the directory
set in :code:`DATAPORTEN_CACHE_PATH` before starting the Django server.

.. code:: python

    # Cache requests to the dataporten API
    DATAPORTEN_CACHE_REQUESTS = True

    # Where to save the sqlite3 cache backend
    DATAPORTEN_CACHE_PATH = 'tmp/'

.. _django-allauth: https://github.com/pennersr/django-allauth:


Usage
-----

The :code:`DataportenGroupsMiddleware` adds an instance of
:code:`DataportenGroupsManager` saved to :code:`request.user.dataporten` for
every valid dataporten users.

You can check if a group is an **active** member of a specific dataporten group
by providing the group :code:`id` to the
:code:`DataportenGroupsManager.is_member_of` method. For instance,

.. code:: python

    assert request.user.dataporten.is_member_of(
        uid='fc:org:ntnu.no:unit:167500',
        active=True,
    )

If :code:`active` is set to :code:`False`, the method only checks if the user
has been a member of the group at any time, not necessarily if the user is
an **active** member.

You can also check if a user has any affiliation to a course, only given
its course code, and not its dataporten ID,

.. code:: python

    # Already finished the course
    assert 'TMA4150' in request.user.dataporten.courses.finished

    # Currently enrolled in the course
    assert 'TMA4150' in request.user.dataporten.courses.active

    # Either
    assert 'TMA4150' in request.user.dataporten.courses.all


There is still lots of more undocumented (but well tested!) attributes of
:code:`DataportenGroupsManager`. Take a look at :code:`dataporten/parsers.py`.
Each parser has a class variable :code:`NAME`, and they are attached to
the user as :code:`request.user.dataporten.NAME`.

If you have a specific usecase, please open a GitHub issue, and I will
document and/or implement it for you.

Run tests
_________

.. code:: bash

    export DJANGO_SETTINGS_MODULE=dataporten.settings
    pytest
