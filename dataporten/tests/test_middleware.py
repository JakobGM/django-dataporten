from unittest.mock import Mock

from django.contrib.auth.models import AnonymousUser, User

import pytest

from ..middleware import DataportenGroupsMiddleware
from ..models import DataportenUser


def test_dataporten_middleware_with_anonymous_user(rf, monkeypatch):
    request = rf.get('')
    dpm = DataportenGroupsMiddleware(Mock())

    request.user = AnonymousUser()
    dpm(request)
    assert type(request.user) is AnonymousUser


@pytest.mark.django_db
def test_dataporten_middleware_with_plain_django_user(
    rf,
    django_user_model,
    monkeypatch,
):
    request = rf.get('')
    dpm = DataportenGroupsMiddleware(Mock())

    request.user = django_user_model()
    dpm(request)
    assert type(request.user) is User


@pytest.mark.django_db
def test_dataporten_middleware_with_user_with_dataporten_credentials(
    rf,
    user_with_dataporten_token,
    monkeypatch,
):
    request = rf.get('')
    dpm = DataportenGroupsMiddleware(Mock())

    request.user = user_with_dataporten_token
    dpm(request)
    assert type(request.user) is DataportenUser
