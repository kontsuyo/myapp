import logging

import pytest

from users.models import Account
from users.serializers import RegisterSerializer

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_register_serializer_valid_data():
    data = {
        "username": "testuser",
        "password": "strongpassword",
        "password_confirm": "strongpassword",
    }
    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()
    assert user.username == data["username"]
    assert user.check_password(data["password"])
    assert Account.objects.filter(username=data["username"]).exists()


@pytest.mark.django_db
def test_register_serializer_password_mismatch():
    data = {
        "username": "testuser",
        "password": "strongpassword",
        "password_confirm": "wrongpassword",
    }
    serializer = RegisterSerializer(data=data)
    assert not serializer.is_valid()
    assert "パスワードが間違っています。" in str(serializer.errors)


@pytest.mark.django_db
def test_register_serializer_missing_fields():
    data = {
        "username": "testuser",
        "password": "strongpassword",
    }
    serializer = RegisterSerializer(data=data)
    assert not serializer.is_valid()
    assert "この項目は必須です。" in str(serializer.errors["password_confirm"])


@pytest.mark.django_db
def test_register_serializer_password_too_short():
    data = {
        "username": "testuser",
        "password": "short",
        "password_confirm": "short",
    }
    serializer = RegisterSerializer(data=data)
    assert not serializer.is_valid()
    assert "8文字以上のパスワードを入力してください。" in str(
        serializer.errors["password"]
    )


@pytest.mark.django_db
def test_register_serializer_empty_fields():
    data = {
        "username": "",
        "password": "",
        "password_confirm": "",
    }
    serializer = RegisterSerializer(data=data)
    assert not serializer.is_valid()
    logger.debug(serializer.errors)
    assert "この項目は空にできません。" in str(serializer.errors["username"])
    assert "この項目は空にできません。" in str(serializer.errors["password"])
    assert "この項目は空にできません。" in str(serializer.errors["password_confirm"])


@pytest.mark.django_db
def test_register_serializer_invalid_username():
    data = {
        "username": "invalid-name",
        "password": "strongpassword",
        "password_confirm": "strongpassword",
    }
    serializer = RegisterSerializer(data=data)
    assert not serializer.is_valid()
    assert "ユーザ名は英数字と'_'(アンダーバー)が使えます" in str(
        serializer.errors["username"]
    )


@pytest.mark.django_db
def test_register_serializer_username_too_short():
    data = {
        "username": "usr",
        "password": "strongpassword",
        "password_confirm": "strongpassword",
    }
    serializer = RegisterSerializer(data=data)
    assert not serializer.is_valid()
    assert "username" in serializer.errors
    assert "ユーザ名は4文字以上にしてください。" in str(serializer.errors["username"])


@pytest.mark.django_db
def test_register_serializer_username_too_long():
    data = {
        "username": "thisisaverylongusername",
        "password": "strongpassword",
        "password_confirm": "strongpassword",
    }
    serializer = RegisterSerializer(data=data)
    assert not serializer.is_valid()
    assert "username" in serializer.errors
    assert "ユーザー名は15文字までにしてください。" in str(
        serializer.errors["username"]
    )


@pytest.mark.django_db
def test_register_serializer_password_write_only():
    data = {
        "username": "testuser",
        "password": "strongpassword",
        "password_confirm": "strongpassword",
    }
    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid()
    assert "password" not in serializer.data
    assert "password_confirm" not in serializer.data


@pytest.mark.django_db
def test_register_serializer_existing_username():
    Account.objects.create_user(username="existinguser", password="password123")
    data = {
        "username": "existinguser",
        "password": "strongpassword",
        "password_confirm": "strongpassword",
    }
    serializer = RegisterSerializer(data=data)
    assert not serializer.is_valid()
    assert "ユーザー名は使われています。他のものを選んでください" in str(
        serializer.errors["username"]
    )
