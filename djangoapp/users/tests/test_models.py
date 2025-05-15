import logging

import pytest
from django.db import IntegrityError
from django.db.utils import DataError
from rest_framework.authtoken.models import Token

from users.models import Account

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_account_creation():
    user = Account.objects.create_user(username="testuser", password="password123")
    assert user.username == "testuser"
    assert user.check_password("password123")


@pytest.mark.django_db
def test_account_username_unique_constraint():
    Account.objects.create_user(username="uniqueuser", password="password123")

    with pytest.raises(IntegrityError) as excinfo:
        Account.objects.create_user(username="uniqueuser", password="password456")
    assert "duplicate key value violates unique constraint" in str(excinfo.value)


@pytest.mark.django_db
def test_account_str_representation():
    user = Account.objects.create_user(username="testuser", password="password123")
    assert str(user) == "testuser"


@pytest.mark.django_db
def test_account_creation_with_long_username():
    with pytest.raises(DataError) as excinfo:
        Account.objects.create_user(
            username="toolongusername123", password="password123"
        )
    assert "value too long for type character varying(15)" in str(excinfo.value)


@pytest.mark.django_db
def test_account_creation_without_username():
    with pytest.raises(ValueError) as excinfo:
        Account.objects.create_user(username="", password="password123")
    assert "The given username must be set" in str(excinfo.value)


@pytest.mark.django_db
def test_account_password_storaged_hash():
    user = Account.objects.create_user(username="testuser", password="password123")
    assert user.password != "password123"
    assert user.check_password("password123")


@pytest.mark.django_db
def test_account_superuser_creation():
    superuser = Account.objects.create_superuser(
        username="adminuser",
        password="adminpassword",
        email="",
    )
    assert superuser.is_superuser
    assert superuser.is_staff
    assert superuser.check_password("adminpassword")


@pytest.mark.django_db
def test_account_create_auth_token():
    user = Account.objects.create_user(username="testuser", password="password123")
    token = Token.objects.get(user=user)
    assert token.key is not None, "ユーザー作成時にトークンが生成されていません"
    assert token.user == user
