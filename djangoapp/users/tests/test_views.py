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
