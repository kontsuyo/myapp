import logging

import pytest

from users.models import Account, Profile
from users.serializers import (
    AccountUpdateSerializer,
    LoginSerializer,
    ProfileSerializer,
    RegisterSerializer,
    UserSerializer,
)

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


def test_register_serializer_empty_fields():
    data = {
        "username": "",
        "password": "",
        "password_confirm": "",
    }
    serializer = RegisterSerializer(data=data)
    assert not serializer.is_valid()
    logger.debug(serializer.errors)
    assert "ユーザー名を入力してください。" in str(serializer.errors["username"])
    assert "パスワードを入力してください。" in str(serializer.errors["password"])
    assert "確認用パスワードを入力してください。" in str(
        serializer.errors["password_confirm"]
    )


@pytest.mark.django_db
def test_register_serializer_invalid_username():
    data = {
        "username": "invalid-name",
        "password": "strongpassword",
        "password_confirm": "strongpassword",
    }
    serializer = RegisterSerializer(data=data)
    assert not serializer.is_valid()
    assert "ユーザー名は英数字と'_'(アンダーバー)が使えます" in str(
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
    assert "ユーザー名は4文字以上にしてください。" in str(serializer.errors["username"])


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


@pytest.mark.django_db
def test_login_serializer_valid_data():
    Account.objects.create_user(username="testuser", password="strongpassword")
    data = {
        "username": "testuser",
        "password": "strongpassword",
    }
    serializer = LoginSerializer(data=data)
    assert serializer.is_valid(), serializer.errors


def test_login_serializer_empty_fields():
    data = {
        "username": "",
        "password": "",
    }
    serializer = LoginSerializer(data=data)
    assert not serializer.is_valid()
    assert "ユーザー名を入力してください。" in str(serializer.errors["username"])
    assert "パスワードを入力してください。" in str(serializer.errors["password"])


@pytest.mark.django_db
def test_login_serializer_nonexistent_user():
    data = {
        "username": "nonexistentuser",
        "password": "strongpassword",
    }
    serializer = LoginSerializer(data=data)
    assert not serializer.is_valid()
    assert "ユーザー名が正しくありません。" in str(serializer.errors["username"])


@pytest.mark.django_db
def test_login_serializer_incorrect_password():
    Account.objects.create_user(username="testuser", password="strongpassword")
    data = {
        "username": "testuser",
        "password": "wrongpassword",
    }
    serializer = LoginSerializer(data=data)
    assert not serializer.is_valid()
    assert "パスワードが正しくありません。" in str(serializer.errors["password"])


@pytest.mark.django_db
def test_login_serializer_invalid_username():
    data = {
        "username": "invalid!name",
        "password": "strongpassword",
    }
    serializer = LoginSerializer(data=data)
    assert not serializer.is_valid()
    assert "ユーザー名が正しくありません。" in str(serializer.errors["username"])


@pytest.mark.django_db
def test_account_update_serializer_valid_data():
    user = Account.objects.create_user(username="testuser", password="strongpassword")
    data = {
        "username": "updateusername",
    }

    serializer = AccountUpdateSerializer(instance=user, data=data)
    assert serializer.is_valid(), serializer.errors
    updateuser = serializer.save()
    assert updateuser.username == data["username"]
    assert Account.objects.filter(username=data["username"]).exists()
    assert user.id == updateuser.id  # type: ignore


@pytest.mark.django_db
def test_account_update_serializer_empty_fields():
    user = Account.objects.create_user(username="testuser", password="strongpassword")
    data = {
        "username": "",
    }
    serializer = AccountUpdateSerializer(instance=user, data=data)
    assert not serializer.is_valid()
    assert "ユーザー名を入力してください。" in str(serializer.errors["username"])


@pytest.mark.django_db
def test_account_update_serializer_username_too_short():
    user = Account.objects.create_user(username="testuser", password="strongpassword")
    data = {
        "username": "usr",
    }
    serializer = AccountUpdateSerializer(instance=user, data=data)
    assert not serializer.is_valid()
    assert "ユーザー名は4文字以上にしてください。" in str(serializer.errors["username"])


@pytest.mark.django_db
def test_account_update_serializer_username_too_long():
    user = Account.objects.create_user(username="testuser", password="strongpassword")
    data = {
        "username": "thisisaverylongusername",
    }
    serializer = AccountUpdateSerializer(instance=user, data=data)
    assert not serializer.is_valid()
    assert "ユーザー名は15文字までにしてください。" in str(
        serializer.errors["username"]
    )


@pytest.mark.django_db
def test_account_update_serializer_invalid_username():
    user = Account.objects.create_user(username="testuser", password="strongpassword")
    data = {
        "username": "invalid-name",
    }
    serializer = AccountUpdateSerializer(instance=user, data=data)
    assert not serializer.is_valid()
    assert "ユーザー名は英数字と'_'(アンダーバー)が使えます" in str(
        serializer.errors["username"]
    )


@pytest.mark.django_db
def test_account_update_serializer_username_already_exists():
    Account.objects.create_user(username="existinguser", password="password123")
    user = Account.objects.create_user(username="testuser", password="strongpassword")
    data = {
        "username": "existinguser",
    }
    serializer = AccountUpdateSerializer(instance=user, data=data)
    assert not serializer.is_valid()
    assert "ユーザー名は使われています。他のものを選んでください" in str(
        serializer.errors["username"]
    )


@pytest.mark.django_db
def test_user_serializer_output():
    user = Account.objects.create_user(username="testuser", password="strongpassword")
    serializer = UserSerializer(user)
    assert serializer.data["username"] == "testuser"


@pytest.mark.django_db
def test_user_serializer_read_only_fields():
    user = Account.objects.create_user(username="testuser", password="strongpassword")
    input_data = {
        "username": "newusername",
    }
    serializer = UserSerializer(instance=user, data=input_data, partial=True)
    assert serializer.is_valid(), serializer.errors
    updated_user = serializer.save()
    assert updated_user.username == "testuser"


@pytest.mark.django_db
def test_profile_serializer_output():
    user = Account.objects.create_user(username="testuser", password="password123")
    profile = Profile.objects.get(user=user)
    data = {
        "handle": "handle",
        "bio": "bio",
        "profile_image": None,  # Assuming no image for simplicity
        "place": "tokyo",
        "website": "https://example.com",
    }
    serializer = ProfileSerializer(instance=profile, data=data, partial=True)
    assert serializer.is_valid(), serializer.errors
    serializer.save()
    data = serializer.data
    assert data["user"]["username"] == "testuser"
    assert data["handle"] == "handle"
    assert data["bio"] == "bio"
    assert data["place"] == "tokyo"


@pytest.mark.django_db
def test_profile_serializer_user_read_only():
    user = Account.objects.create_user(username="testuser", password="password123")
    profile = Profile.objects.get(user=user)
    data = {
        "user": {"username": "newusername"},
    }
    serializer = ProfileSerializer(instance=profile, data=data, partial=True)
    assert serializer.is_valid(), serializer.errors
    serializer.save()
    updated_data = serializer.data
    assert updated_data["user"]["username"] == "testuser"
