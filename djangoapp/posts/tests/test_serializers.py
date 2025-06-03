import pytest
from rest_framework.test import APIRequestFactory

from posts.serializers import PostSerializer


@pytest.mark.django_db
def test_serializer_create_post(user):
    factory = APIRequestFactory()
    request = factory.post("/posts/", {"content": "This is a test post."})
    request.user = user

    serializer = PostSerializer(
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

    serializer = PostSerializer(
        data={"content": ""},
        context={"request": request},
    )
    assert not serializer.is_valid()
    assert "content" in serializer.errors
    assert serializer.errors["content"] == ["この項目は空にできません。"]

    serializer = PostSerializer(
        data={"content": "test", "author": 9999},
        context={"request": request},
    )


@pytest.mark.django_db
def test_post_serializer_author_read_only(user):
    factory = APIRequestFactory()
    request = factory.post("/posts/", {"content": "test"})
    request.user = user

    # authorを入力データで上書きしようとしても無視されることを確認
    serializer = PostSerializer(
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

    serializer = PostSerializer(
        data={"content": "test", "posted_date": "2023-01-01T00:00:00Z"},
        context={"request": request},
    )
    assert serializer.is_valid(), serializer.errors
    post = serializer.save()

    # posted_dateは自動で設定されるため、入力値は無視されることを確認
    assert not post.posted_date == "2023-01-01T00:00:00Z"
    assert post.posted_date is not None
    assert post.author == user
