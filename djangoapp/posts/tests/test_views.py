import logging

import pytest
from django.urls import reverse

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_post_create_view_success(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse("post")
    data = {
        "content": "This is a test post.",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    logger.info(f"Response data: {response.data}")
    assert response.data["post"]["author"] == user.username
    assert response.data["post"]["content"] == "This is a test post."
    assert "posted_date" in response.data["post"]


@pytest.mark.django_db
def test_post_create_view_unauthenticated(api_client):
    url = reverse("post")
    data = {
        "content": "This is a test post.",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 401
    logger.info(f"Response data: {response.data}")
    assert response.data["detail"] == "認証情報が含まれていません。"


@pytest.mark.django_db
def test_post_create_view_token_authentication(api_client, user):
    token = user.auth_token.key
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    url = reverse("post")
    data = {
        "content": "This is a test post with token authentication.",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    logger.info(f"Response data: {response.data}")
    assert response.data["post"]["author"] == user.username
    assert response.data["post"]["content"] == "This is a test post with token authentication."
    assert "posted_date" in response.data["post"]


@pytest.mark.django_db
def test_post_create_view_invalid_data(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse("post")
    data = {
        "content": "",  # Invalid content
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
    logger.info(f"Response data: {response.data}")
    assert "この項目は空にできません。" in str(response.data["content"])
