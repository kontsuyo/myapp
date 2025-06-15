import pytest
from rest_framework.test import APIClient

from posts.models import Post
from users.models import Account


@pytest.fixture
def user():
    return Account.objects.create_user(username="user1", password="testpassword")


@pytest.fixture
def other_user():
    return Account.objects.create_user(username="user2", password="testpassword")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def post_data():
    return {"content": "This is a test post."}


@pytest.fixture
def post(user, post_data):
    return Post.objects.create(author=user, content=post_data["content"])


@pytest.fixture
def other_post(other_user, post_data):
    return Post.objects.create(author=other_user, content=post_data["content"])


@pytest.fixture
def users():
    return [Account.objects.create_user(username=f"testuser{i}", password="testpassword") for i in range(5)]


@pytest.fixture
def posts(users):
    # 各ユーザーに5件ずつポストを作成
    return [
        Post.objects.create(author=user, content=f"Post for {user.username} #{i}") for user in users for i in range(5)
    ]
