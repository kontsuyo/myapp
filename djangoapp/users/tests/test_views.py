import logging

import pytest
from django.urls import reverse

from users.models import Account

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_user_registration_success(api_client):
    url = reverse("register")
    data = {
        "username": "newuser",
        "password": "securepassword",
        "password_confirm": "securepassword",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    assert response.data["message"] == "ユーザー登録が完了しました。"
    assert Account.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_user_registration_password_mismatch(api_client):
    url = reverse("register")
    data = {
        "username": "newuser",
        "password": "securepassword",
        "password_confirm": "wrongpassword",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
    assert "パスワードが間違っています。" in str(response.data)


@pytest.mark.django_db
def test_user_registration_duplicate_username(api_client):
    Account.objects.create_user(username="existinguser", password="password123")
    url = reverse("register")
    data = {
        "username": "existinguser",
        "password": "securepassword",
        "password_confirm": "securepassword",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
    assert "ユーザー名は使われています。他のものを選んでください" in str(response.data)


@pytest.mark.django_db
def test_user_registration_empty_fields(api_client):
    url = reverse("register")
    data = {
        "username": "",
        "password": "",
        "password_confirm": "",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
    assert "ユーザー名を入力してください。" in str(
        response.data["username"]
    )
    assert "パスワードを入力してください。" in str(
        response.data["password"]
    )
    assert "確認用パスワードを入力してください。" in str(
        response.data["password_confirm"]
    )


@pytest.mark.django_db
def test_user_login_success(api_client):
    Account.objects.create_user(username="testuser", password="securepassword")
    url = reverse("login")
    data = {
        "username": "testuser",
        "password": "securepassword",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 200
    assert response.data["message"] == "ログインに成功しました。"
    assert "token" in response.data
    assert response.data["username"] == "testuser"


@pytest.mark.django_db
def test_user_login_invalid_username(api_client):
    Account.objects.create_user(username="testuser", password="securepassword")
    url = reverse("login")
    data = {
        "username": "wronguser",
        "password": "securepassword",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
    assert "ユーザー名が正しくありません。" in str(response.data)


@pytest.mark.django_db
def test_user_login_invalid_password(api_client):
    Account.objects.create_user(username="testuser", password="securepassword")
    url = reverse("login")
    data = {
        "username": "testuser",
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
