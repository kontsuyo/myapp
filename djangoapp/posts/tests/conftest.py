import pytest
from rest_framework.test import APIClient

from posts.models import Post
from users.models import Account


@pytest.fixture
def user():
    return Account.objects.create_user(
        username="testuser",
        password="testpassword",
    )


@pytest.fixture
def other_user():
    return Account.objects.create_user(
        username="otheruser",
        password="otherpassword",
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def post_data():
    return {
        "content": "This is a test post.",
    }


@pytest.fixture
def post(user, post_data):
    return Post.objects.create(author=user, **post_data)


@pytest.fixture
def other_post(other_user, post_data):
    return Post.objects.create(author=other_user, **post_data)
