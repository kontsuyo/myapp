import logging
from datetime import timedelta

import pytest
from rest_framework.test import APIRequestFactory

from posts.models import Post
from posts.serializers import PostCreateSerializer, PostUpdateSerializer

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_serializer_create_post(user):
    factory = APIRequestFactory()
    request = factory.post("/posts/", {"content": "This is a test post."})
    request.user = user

    serializer = PostCreateSerializer(
        data={"content": "This is a test post."},
        context={"request": request},
    )
    assert serializer.is_valid(), serializer.errors
    post = serializer.save()
    assert post.author == user
    assert post.content == "This is a test post."


@pytest.mark.django_db
def test_serializer_create_post_empty_content(user):
    factory = APIRequestFactory()
    request = factory.post("/posts/", {"content": ""})
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
def test_post_serializer_author_read_only(user):
    factory = APIRequestFactory()
    request = factory.post("/posts/", {"content": "test"})
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
def test_post_serializer_posted_date_read_only(user):
    factory = APIRequestFactory()
    request = factory.post("/posts/", {"content": "test"})
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
def test_post_update_serializer_valid_data(user):

    post = Post.objects.create(author=user, content="Initial content")

    serializer = PostUpdateSerializer(
        instance=post,
        data={"content": "Updated content"},
        partial=True,
    )
    assert serializer.is_valid(), serializer.errors
    updated_post = serializer.save()
    assert updated_post.content == "Updated content"


@pytest.mark.django_db
def test_post_update_serializer_read_only_fields(user):
    post = Post.objects.create(author=user, content="Initial content")

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
def test_post_update_serializer_edit_before_30_minutes(user):
    post = Post.objects.create(author=user, content="Initial content")
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
def test_post_update_serializer_edit_after_30_minutes(user):
    post = Post.objects.create(author=user, content="Initial content")
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
