=================
Django-dataporten
=================

Django-dataporten is a simple Django app which fetches data from dataporten and
attaches it to your Django user objects. It implements the dataporten groups
API, allowing you to easily access group memberships through a pythonic API, without
worrying about parsing raw JSON content.

Setup
=====

1. Add "dataporten" to your :code:`INSTALLED_APPS` setting like this

.. code:: python

    INSTALLED_APPS = [
        ...
        'dataporten',
        ...
    ]


2. Run `python manage.py migrate` to create the dataporten proxy models.

3. In your `settings.py` file, add the variable :code:`DATAPORTEN_TOKEN_FUNCTION`,
which should be a dotted path to the function that will retrieve user tokens.
Dataporten uses this "importable string" in order to retrieve the OAuth2
authentication token for a given user. For instance,

.. code:: python

    DATAPORTEN_TOKEN_FUNCTION = 'myapp.oauth.allauth_token'

The function should accept a :code:`User` and return a :code:`str`, if the
token exists, else :code:`None`.
Here is a python3.6/3.7 example that will work if you use `django-allauth`_:

.. code:: python

    def allauth_token(user: User) -> Optional[str]:
        try:
            return SocialToken.objects.get(
                account__user=user,
                account__provider='dataporten',
            ).token
        except SocialToken.DoesNotExist:
            return None

4. Add the dataporten middleware. This middleware adds a :code:`dataporten`
attribute to :code:`request.user` for users with an associated
dataporten token. Take care to place it after
:code:`django.contrib.auth.middleware.AuthenticationMiddleware`.

.. code:: python

    MIDDLEWARE = (
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        ...
        'dataporten.middleware.DataportenGroupsMiddleware',
        ...
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
=====

The :code:`DataportenGroupsMiddleware` adds an instance of
:code:`DataportenGroupsManager` assigned to :code:`request.user.dataporten` for
every valid dataporten user making a request. This object contains attributes
for accessing different types of group memberships, such as courses, organization
units, study programmes, main profiles, generic groups, and *all* groups.


Groups
------

*All* groups are accessible through :code:`request.user.dataporten.groups`.
This is a dictionary keyed by group ids, with :code:`Group` objects as values.
Let's use the Applied Physics and Mathematics master degree at NTNU as an example
for common attributes available for all group types

.. code:: python

    uid = 'fc:fs:fs:prg:ntnu.no:MTFYMA'
    group = request.user.dataporten.groups[uid]
    assert group.uid == uid
    assert group.name == 'Fysikk og matematikk - masterstudium (5-\u00e5rig)'
    assert group.url == 'http://www.ntnu.no/studier/mtfyma'
    assert group.group_type == 'fc:fs:prg'

Membership objects
------------------

All groups have an associated :code:`Membership` object which can be used for
further querying of membership properties for that particular group

.. code:: python

    group = request.user.dataporten.groups[uid]
    membership = group.membership

    # Membership objects are "truthy" if they are considered active
    assert membership

    # Not all group memberships have a set end time
    assert isinstance(membership.end_time, [datetime.datetime, None])

Group membership checks
~~~~~~~~~~~~~~~~~~~~~~~

You can also check if a user is an **active** member of a specific dataporten group
by providing the group :code:`id` to the :code:`DataportenGroupsManager.is_member_of`
method. This is offered as a more ergonomic alternative to
:code:`bool(request.user.dataporten.groups[uid].membership)`. For instance,

.. code:: python

    assert request.user.dataporten.is_member_of(
        uid='fc:org:ntnu.no:unit:167500',
        active=True,
    )

If :code:`active` is set to :code:`False`, the method only checks if the user
has been a member of the group at any time, not necessarily if the user is
an **active** member.

Semester objects
----------------

Membership objects also have an associated :code:`Semester` object which
can be used to determine the year and season of the membership.

.. code:: python

    from dataporten.parsers import Semester

    semester = request.user.groups[uid].membership.semester
    assert semester.year == 2019
    assert semester.season in (Semester.SPRING, Semester.AUTUMN)

The :code:`Semester` class also implements :code:`__sub__`, which
returns "semester delta" between two semesters. For instance,
the spring semester of 2019 minus the autumn semester of 2017 would
return :code:`3`.

Courses
-------

Course enrollment can be queryed from the :code:`CourseManager` object, attributed to
:code:`request.user.dataporten.course`.

You can check if a user has an affiliation to a course, only given
its course code, and not its dataporten ID,

.. code:: python

    # Already finished the course
    assert 'TMA4150' in request.user.dataporten.courses.finished

    # Currently enrolled in the course
    assert 'TMA4150' in request.user.dataporten.courses.active

    # Either
    assert 'TMA4150' in request.user.dataporten.courses.all


More
----

There is still lots of more undocumented (but well tested!) attributes of
:code:`DataportenGroupsManager`. Take a look at :code:`dataporten/parsers.py`.
Each parser has a class variable :code:`NAME`, and they are attached to
the user as :code:`request.user.dataporten.NAME`.

If you have a specific usecase, please open a GitHub issue, and I will
document and/or implement it for you.

Run tests
=========

.. code:: bash

    export DJANGO_SETTINGS_MODULE=dataporten.settings
    pytest
