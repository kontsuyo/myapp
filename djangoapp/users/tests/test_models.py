import io
import logging

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.db.utils import DataError
from rest_framework.authtoken.models import Token

from users.models import Account, Profile

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
        Account.objects.create_user(username="toolongusername123", password="password123")
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


@pytest.mark.django_db
def test_profile_creation():
    user = Account.objects.create_user(username="testuser", password="password123")
    assert user.profile.user == user  # pyright:ignore[reportAttributeAccessIssue]
    assert user.profile.handle == ""  # pyright:ignore[reportAttributeAccessIssue]
    assert user.profile.bio == ""  # pyright:ignore[reportAttributeAccessIssue]
    assert user.profile.place == ""  # pyright:ignore[reportAttributeAccessIssue]
    assert user.profile.website == ""  # pyright:ignore[reportAttributeAccessIssue]


@pytest.mark.django_db
def test_profile_image_upload():
    user = Account.objects.create_user(username="testuser", password="password123")
    profile = user.profile  # pyright:ignore[reportAttributeAccessIssue]
    image_content = b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b"
    image_file = SimpleUploadedFile("test_image.gif", io.BytesIO(image_content).getvalue(), content_type="image/gif")
    profile.profile_image.save("test_image.gif", image_file, save=True)
    assert profile.profile_image.name.startswith("profile_images/test_image.gif")
    profile.profile_image.delete(save=False)


@pytest.mark.django_db
def test_profile_handle_max_length():
    user = Account.objects.create_user(username="testuser", password="password123")
    profile = user.profile  # pyright:ignore[reportAttributeAccessIssue]
    profile.handle = "a" * 51
    with pytest.raises(DataError) as excinfo:
        profile.save()
    assert "value too long for type character varying(50)" in str(excinfo.value)


@pytest.mark.django_db
def test_profile_bio_max_length():
    user = Account.objects.create_user(username="testuser", password="password123")
    profile = user.profile  # pyright:ignore[reportAttributeAccessIssue]
    profile.bio = "b" * 161
    with pytest.raises(ValueError) as excinfo:
        profile.save()
    assert "value too long for type character varying(160)" in str(excinfo.value)


@pytest.mark.django_db
def test_profile_place_max_length():
    user = Account.objects.create_user(username="testuser", password="password123")
    profile = user.profile  # pyright:ignore[reportAttributeAccessIssue]
    profile.place = "c" * 31
    with pytest.raises(DataError) as excinfo:
        profile.save()
    assert "value too long for type character varying(30)" in str(excinfo.value)


@pytest.mark.django_db
def test_profile_website_max_length():
    user = Account.objects.create_user(username="testuser", password="password123")
    profile = user.profile  # pyright:ignore[reportAttributeAccessIssue]
    profile.website = "https://example.com/" + "d" * 101
    with pytest.raises(DataError) as excinfo:
        profile.save()
    assert "value too long for type character varying(100)" in str(excinfo.value)


@pytest.mark.django_db
def test_profile_deleted_when_user_deleted():
    user = Account.objects.create_user(username="testuser", password="password123")
    profile_id = user.profile.id  # pyright:ignore[reportAttributeAccessIssue]
    user.delete()
    assert not Profile.objects.filter(id=profile_id).exists()
