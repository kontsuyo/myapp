import logging

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token

from users.models import Account

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_user_registration_success(api_client):
    url = reverse("register-account")
    data = {
        "username": "newuser",
        "password": "securepassword",
        "password_confirm": "securepassword",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    assert response.data["message"] == "ユーザー登録が完了しました。"
    assert "token" in response.data
    assert response.data["username"] == "newuser"
    assert Account.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_user_registration_password_mismatch(api_client):
    url = reverse("register-account")
    data = {
        "username": "newuser",
        "password": "securepassword",
        "password_confirm": "wrongpassword",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
    assert "パスワードが間違っています。" in str(response.data)


@pytest.mark.django_db
def test_user_registration_duplicate_username(api_client, user):
    url = reverse("register-account")
    data = {
        "username": user.username,
        "password": "securepassword",
        "password_confirm": "securepassword",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
    assert "ユーザー名は使われています。他のものを選んでください" in str(response.data)


@pytest.mark.django_db
def test_user_registration_empty_fields(api_client):
    url = reverse("register-account")
    data = {
        "username": "",
        "password": "",
        "password_confirm": "",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
    assert "ユーザー名を入力してください。" in str(response.data["username"])
    assert "パスワードを入力してください。" in str(response.data["password"])
    assert "確認用パスワードを入力してください。" in str(response.data["password_confirm"])


@pytest.mark.django_db
def test_user_login_success(api_client, user):
    url = reverse("login")
    data = {
        "username": user.username,
        "password": "testpassword",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 200
    assert response.data["message"] == "ログインに成功しました。"
    assert "token" in response.data
    assert response.data["username"] == "testuser"


@pytest.mark.django_db
def test_user_login_invalid_username(api_client, user):
    url = reverse("login")
    data = {
        "username": "wronguser",
        "password": "securepassword",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
    assert "ユーザー名が正しくありません。" in str(response.data)


@pytest.mark.django_db
def test_user_login_invalid_password(api_client, user):
    url = reverse("login")
    data = {
        "username": user.username,
        "password": "wrongpassword",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
    assert "パスワードが正しくありません。" in str(response.data)


@pytest.mark.django_db
def test_user_login_nonexistent_user(api_client):
    url = reverse("login")
    data = {
        "username": "nonexistentuser",
        "password": "securepassword",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
    assert "ユーザー名が正しくありません。" in str(response.data)


@pytest.mark.django_db
def test_user_login_empty_fields(api_client):
    url = reverse("login")
    data = {
        "username": "",
        "password": "",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
    assert "ユーザー名を入力してください。" in str(response.data["username"])
    assert "パスワードを入力してください。" in str(response.data["password"])


@pytest.mark.django_db
def test_user_account_update_success(api_client, user):
    url = reverse("update-account")
    api_client.force_authenticate(user=user)
    data = {
        "username": "updateduser",
    }
    response = api_client.patch(url, data, format="json")
    assert response.status_code == 200
    assert response.data["message"] == "ユーザー情報が更新されました。"
    assert response.data["username"] == "updateduser"


@pytest.mark.django_db
def test_user_account_update_invalid_username(api_client, user):
    url = reverse("update-account")
    api_client.force_authenticate(user=user)
    data = {
        "username": "invalid name",
    }
    response = api_client.patch(url, data, format="json")
    assert response.status_code == 400
    assert "ユーザー名は英数字と'_'(アンダーバー)が使えます" in str(response.data["username"])


@pytest.mark.django_db
def test_user_account_update_duplicate_username(api_client, user):
    Account.objects.create_user(username="existinguser", password="securepassword")
    url = reverse("update-account")
    api_client.force_authenticate(user=user)
    data = {
        "username": "existinguser",
    }
    response = api_client.patch(url, data, format="json")
    assert response.status_code == 400
    assert "ユーザー名は使われています。他のものを選んでください" in str(response.data["username"])


@pytest.mark.django_db
def test_user_account_update_empty_fields(api_client, user):
    url = reverse("update-account")
    api_client.force_authenticate(user=user)
    data = {
        "username": "",
    }
    response = api_client.patch(url, data, format="json")
    assert response.status_code == 400
    assert "ユーザー名を入力してください。" in str(response.data["username"])


@pytest.mark.django_db
def test_user_account_update_requires_authentication(api_client):
    url = reverse("update-account")
    data = {
        "username": "updateduser",
    }
    response = api_client.patch(url, data, format="json")
    assert response.status_code == 401
    assert response.data["detail"] == "認証情報が含まれていません。"


@pytest.mark.django_db
def test_user_account_update_authenticated_user(api_client, user):
    url = reverse("update-account")
    token, _ = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    data = {
        "username": "updateduser",
    }
    response = api_client.patch(url, data, format="json")
    assert response.status_code == 200
    assert response.data["message"] == "ユーザー情報が更新されました。"
    assert response.data["username"] == "updateduser"


@pytest.mark.django_db
def test_user_account_delete_success(api_client, user):
    url = reverse("delete-account")
    api_client.force_authenticate(user=user)
    response = api_client.delete(url, format="json")
    assert response.status_code == 200
    assert response.data["message"] == "ユーザーが削除されました。"
    assert not Account.objects.filter(username=user.username).exists()


@pytest.mark.django_db
def test_account_delete_requires_authentication(api_client):
    url = reverse("delete-account")
    response = api_client.delete(url)
    assert response.status_code == 401
    assert "認証情報が含まれていません。" in str(response.data["detail"])


@pytest.mark.django_db
def test_account_delete_authenticated_user(api_client, user):
    url = reverse("delete-account")
    token, _ = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = api_client.delete(url)
    assert response.status_code == 200
    assert response.data["message"] == "ユーザーが削除されました。"


@pytest.mark.django_db
def test_profile_get_success(api_client, user):
    url = reverse("profile")
    api_client.force_authenticate(user=user)
    response = api_client.get(url, format="json")
    assert response.status_code == 200
    assert "handle" in response.data
    assert "bio" in response.data
    assert "profile_image" in response.data
    assert "place" in response.data
    assert "website" in response.data


@pytest.mark.django_db
def test_profile_patch_success(api_client, user):
    url = reverse("profile")
    api_client.force_authenticate(user=user)
    data = {
        "handle": "Updated Handle",
        "bio": "Updated bio.",
        "place": "Updated Place",
        "website": "https://updateduser.com",
    }
    response = api_client.patch(url, data, format="json")
    assert response.status_code == 200
    assert response.data["user"]["username"] == user.username
    assert response.data["handle"] == "Updated Handle"
    assert response.data["bio"] == "Updated bio."
    assert response.data["place"] == "Updated Place"
    assert response.data["website"] == "https://updateduser.com"


@pytest.mark.django_db
def test_profile_patch_requires_authentication(api_client):
    url = reverse("profile")
    data = {
        "handle": "Updated Handle",
        "bio": "Updated bio.",
        "place": "Updated Place",
        "website": "https://updateduser.com",
    }
    response = api_client.patch(url, data, format="json")
    assert response.status_code == 401
    assert response.data["detail"] == "認証情報が含まれていません。"
