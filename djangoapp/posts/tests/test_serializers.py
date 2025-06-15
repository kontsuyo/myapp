import logging
from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIRequestFactory

from posts.serializers import (
    PostCreateSerializer,
    PostListSerializer,
    PostRetrieveSerializer,
    PostUpdateSerializer,
)

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_post_create_serializer_valid_data(user, post_data):
    factory = APIRequestFactory()
    url = reverse("post")
    request = factory.post(url, post_data)
    request.user = user

    serializer = PostCreateSerializer(
        data=post_data,
        context={"request": request},
    )
    assert serializer.is_valid(), serializer.errors
    post = serializer.save()
    assert post.author == user
    assert post.content == "This is a test post."


@pytest.mark.django_db
def test_post_create_serializer_empty_content(user, post_data):
    factory = APIRequestFactory()
    url = reverse("post")
    request = factory.post(url, post_data)
    request.user = user

    serializer = PostCreateSerializer(
        data={"content": ""},
        context={"request": request},
    )
    assert not serializer.is_valid()
    assert "content" in serializer.errors
    assert serializer.errors["content"] == ["この項目は空にできません。"]

    serializer = PostCreateSerializer(
        data={"content": "test", "author": 9999},
        context={"request": request},
    )


@pytest.mark.django_db
def test_post_create_serializer_author_read_only(user, post_data):
    factory = APIRequestFactory()
    url = reverse("post")
    request = factory.post(url, post_data)
    request.user = user

    # authorを入力データで上書きしようとしても無視されることを確認
    serializer = PostCreateSerializer(
        data={"content": "test", "author": 9999},
        context={"request": request},
    )
    assert serializer.is_valid(), serializer.errors
    post = serializer.save()
    # authorはリクエストユーザーで上書きされている
    assert post.author == user


@pytest.mark.django_db
def test_post_create_serializer_posted_date_read_only(user, post_data):
    factory = APIRequestFactory()
    url = reverse("post")
    request = factory.post(url, post_data)
    request.user = user

    serializer = PostCreateSerializer(
        data={"content": "test", "posted_date": "2023-01-01T00:00:00Z"},
        context={"request": request},
    )
    assert serializer.is_valid(), serializer.errors
    post = serializer.save()

    # posted_dateは自動で設定されるため、入力値は無視されることを確認
    assert not post.posted_date == "2023-01-01T00:00:00Z"
    assert post.posted_date is not None
    assert post.author == user


@pytest.mark.django_db
def test_post_list_serializer_valid_data(post):
    serializer = PostListSerializer(post)
    data = serializer.data
    # posted_dateをJSTに変換して比較
    jst_posted_date = timezone.localtime(post.posted_date).isoformat()
    assert data["posted_date"] == jst_posted_date
    assert data["id"] == post.id
    assert data["author"] == post.author.username
    assert data["content"] == post.content


@pytest.mark.django_db
def test_post_retrieve_serializer_valid_data(post):
    serializer = PostRetrieveSerializer(post)
    data = serializer.data
    # posted_dateをJSTに変換して比較
    jst_posted_date = timezone.localtime(post.posted_date).isoformat()
    assert data["posted_date"] == jst_posted_date
    assert data["id"] == post.id
    assert data["author"] == post.author.username
    assert data["content"] == post.content


@pytest.mark.django_db
def test_post_update_serializer_valid_data(post):
    serializer = PostUpdateSerializer(
        instance=post,
        data={"content": "Updated content"},
        partial=True,
    )
    assert serializer.is_valid(), serializer.errors
    updated_post = serializer.save()
    assert updated_post.content == "Updated content"


@pytest.mark.django_db
def test_post_update_serializer_read_only_fields(user, post):
    serializer = PostUpdateSerializer(
        instance=post,
        data={"author": 9999, "posted_date": "2023-01-01T00:00:00Z"},
        partial=True,
    )
    assert serializer.is_valid(), serializer.errors
    updated_post = serializer.save()

    assert updated_post.author == user
    assert updated_post.posted_date == post.posted_date


@pytest.mark.django_db
def test_post_update_serializer_edit_before_30_minutes(post):
    post.posted_date = post.posted_date - timedelta(minutes=29)
    post.save()

    serializer = PostUpdateSerializer(
        instance=post,
        data={"content": "Updated content"},
        partial=True,
    )
    assert serializer.is_valid(), serializer.errors
    updated_post = serializer.save()
    assert updated_post.content == "Updated content"


@pytest.mark.django_db
def test_post_update_serializer_edit_after_30_minutes(post):
    post.posted_date = post.posted_date - timedelta(minutes=30)
    post.save()

    serializer = PostUpdateSerializer(
        instance=post,
        data={"content": "Updated content"},
        partial=True,
    )
    assert not serializer.is_valid()
    assert "content" in serializer.errors
    assert serializer.errors["content"] == ["投稿の編集は投稿後30分以内のみ可能です。"]
