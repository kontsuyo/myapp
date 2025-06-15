import logging

import pytest
from django.urls import reverse

from posts.models import Post
from users.models import Account

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_post_create_view_success(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse("post")
    data = {"content": "This is a test post."}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    logger.info(f"Response data: {response.data}")
    assert response.data["post"]["author"] == user.username
    assert response.data["post"]["content"] == "This is a test post."
    assert "posted_date" in response.data["post"]


@pytest.mark.django_db
def test_post_create_view_unauthenticated(api_client):
    url = reverse("post")
    data = {"content": "This is a test post."}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 401
    logger.info(f"Response data: {response.data}")
    assert response.data["detail"] == "認証情報が含まれていません。"


@pytest.mark.django_db
def test_post_create_view_token_authentication(api_client, user):
    token = user.auth_token.key
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    url = reverse("post")
    data = {"content": "This is a test post with token authentication."}
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
    data = {"content": ""}  # Invalid content
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
    logger.info(f"Response data: {response.data}")
    assert "この項目は空にできません。" in str(response.data["content"])


@pytest.mark.django_db
def test_post_list_view_success(api_client, user):
    Post.objects.create(author=user, content="First post")
    Post.objects.create(author=user, content="Second post")
    Post.objects.create(author=user, content="Third post")
    url = reverse("post-list", kwargs={"username": user.username})
    response = api_client.get(url, format="json")
    logger.info(f"Response data: {response.data}")
    assert response.status_code == 200
    assert isinstance(response.data, list)


@pytest.mark.django_db
def test_post_list_view_user_not_found(api_client):
    url = reverse("post-list", kwargs={"username": "nonexistentuser"})
    response = api_client.get(url, format="json")
    logger.info(f"Response data: {response.data}")
    assert response.status_code == 404
    assert response.data["detail"] == "User not found."


@pytest.mark.django_db
def test_post_list_view_no_posts(api_client, user):
    url = reverse("post-list", kwargs={"username": user.username})
    response = api_client.get(url, format="json")
    logger.info(f"Response data: {response.data}")
    assert response.status_code == 404
    assert response.data["detail"] == "No posts found for this user."


@pytest.mark.django_db
def test_post_detail_view_success(api_client, user, post):
    url = reverse(
        "post-detail",
        kwargs={
            "username": user.username,
            "post_id": post.id,  # pyright: ignore[reportAttributeAccessIssue]
        },
    )
    response = api_client.get(url, format="json")
    logger.info(f"Response data: {response.data}")
    assert response.status_code == 200
    assert response.data["author"] == user.username
    assert response.data["content"] == post.content
    assert "posted_date" in response.data


@pytest.mark.django_db
def test_post_detail_view_post_not_found(api_client, user):
    url = reverse(
        "post-detail",
        kwargs={
            "username": user.username,
            "post_id": 9999,  # Non-existent post ID
        },
    )
    response = api_client.get(url, format="json")
    logger.info(f"Response data: {response.data}")
    assert response.status_code == 404
    assert response.data["detail"] == "Post not found."


@pytest.mark.django_db
def test_post_detail_view_user_not_found(api_client):
    url = reverse(
        "post-detail",
        kwargs={
            "username": "nonexistentuser",
            "post_id": 1,  # Non-existent user
        },
    )
    response = api_client.get(url, format="json")
    logger.info(f"Response data: {response.data}")
    assert response.status_code == 404
    assert response.data["detail"] == "User not found."


@pytest.mark.django_db
def test_post_update_view_success(api_client, user, post):
    url = reverse(
        "post-update",
        kwargs={
            "username": user.username,
            "post_id": post.id,  # pyright: ignore[reportAttributeAccessIssue]
        },
    )
    api_client.force_authenticate(user=user)
    data = {"content": "Updated content"}
    response = api_client.patch(url, data, format="json")
    logger.info(f"Response data: {response.data}")
    assert response.status_code == 200
    assert response.data["post"]["content"] == "Updated content"


@pytest.mark.django_db
def test_post_update_view_unauthenticated(api_client, user, post):
    url = reverse(
        "post-update",
        kwargs={
            "username": user.username,
            "post_id": post.id,  # pyright: ignore[reportAttributeAccessIssue]
        },
    )
    data = {"content": "Updated content"}
    response = api_client.patch(url, data, format="json")
    logger.info(f"Response data: {response.data}")
    assert response.status_code == 401
    assert response.data["detail"] == "認証情報が含まれていません。"


@pytest.mark.django_db
def test_post_update_view_not_authorized(api_client, user, other_user, other_post):
    url = reverse(
        "post-update",
        kwargs={
            "username": other_user.username,
            "post_id": other_post.id,  # pyright: ignore[reportAttributeAccessIssue]
        },
    )
    api_client.force_authenticate(user=user)
    data = {"content": "Updated content"}
    response = api_client.patch(url, data, format="json")
    logger.info(f"Response data: {response.data}")
    assert response.status_code == 403
    assert response.data["detail"] == "このアクションを実行する権限がありません。"


@pytest.mark.django_db
def test_post_update_view_post_not_found(api_client, user):
    url = reverse(
        "post-update",
        kwargs={
            "username": user.username,
            "post_id": 9999,  # Non-existent post ID
        },
    )
    api_client.force_authenticate(user=user)
    data = {"content": "Updated content"}
    response = api_client.patch(url, data, format="json")
    logger.info(f"Response data: {response.data}")
    assert response.status_code == 404
    assert response.data["detail"] == "Post not found."


@pytest.mark.django_db
def test_post_update_view_user_not_found(api_client):
    url = reverse(
        "post-update",
        kwargs={
            "username": "nonexistentuser",
            "post_id": 1,  # Non-existent user
        },
    )
    api_client.force_authenticate(user=Account.objects.create_user(username="testuser", password="password"))
    data = {"content": "Updated content"}
    response = api_client.patch(url, data, format="json")
    logger.info(f"Response data: {response.data}")
    assert response.status_code == 404
    assert response.data["detail"] == "User not found."


@pytest.mark.django_db
def test_post_delete_view_success(api_client, user, post):
    url = reverse(
        "post-delete",
        kwargs={
            "username": user.username,
            "post_id": post.id,  # pyright: ignore[reportAttributeAccessIssue]
        },
    )
    api_client.force_authenticate(user=user)
    response = api_client.delete(url, format="json")
    logger.info(f"Response data: {response.data}")
    assert response.status_code == 204
    assert not Post.objects.filter(id=post.id).exists()  # pyright: ignore[reportAttributeAccessIssue]


@pytest.mark.django_db
def test_post_delete_view_unauthenticated(api_client, user, post):
    url = reverse(
        "post-delete",
        kwargs={
            "username": user.username,
            "post_id": post.id,  # pyright: ignore[reportAttributeAccessIssue]
        },
    )
    response = api_client.delete(url, format="json")
    logger.info(f"Response data: {response.data}")
    assert response.status_code == 401
    assert response.data["detail"] == "認証情報が含まれていません。"


@pytest.mark.django_db
def test_post_delete_view_not_authorized(api_client, user, other_user, other_post):
    url = reverse(
        "post-delete",
        kwargs={
            "username": other_user.username,
            "post_id": other_post.id,  # pyright: ignore[reportAttributeAccessIssue]
        },
    )
    api_client.force_authenticate(user=user)
    response = api_client.delete(url, format="json")
    logger.info(f"Response data: {response.data}")
    assert response.status_code == 403
    assert response.data["detail"] == "このアクションを実行する権限がありません。"


@pytest.mark.django_db
def test_post_delete_view_post_not_found(api_client, user):
    url = reverse(
        "post-delete",
        kwargs={
            "username": user.username,
            "post_id": 9999,  # Non-existent post ID
        },
    )
    api_client.force_authenticate(user=user)
    response = api_client.delete(url, format="json")
    logger.info(f"Response data: {response.data}")
    assert response.status_code == 404
    assert response.data["detail"] == "Post not found."


@pytest.mark.django_db
def test_post_delete_view_user_not_found(api_client):
    url = reverse(
        "post-delete",
        kwargs={
            "username": "nonexistentuser",
            "post_id": 1,  # Non-existent user
        },
    )
    api_client.force_authenticate(user=Account.objects.create_user(username="testuser", password="password"))
    response = api_client.delete(url, format="json")
    logger.info(f"Response data: {response.data}")
    assert response.status_code == 404
    assert response.data["detail"] == "User not found."
