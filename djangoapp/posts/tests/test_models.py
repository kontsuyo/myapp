import logging

import pytest

from posts.models import Post
from users.models import Account

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_post_post_creation(user, post):
    assert post.author == user
    assert post.content == "This is a test post."
    assert post.posted_date is not None


@pytest.mark.django_db
def test_post_str_method(user, post):
    expected_str = f"Post by {user.username}"
    expected_str = f"{user.username} - {post.posted_date.strftime('%Y-%m-%d %H:%M:%S')}: {post.content[:20]}..."
    assert str(post) == expected_str


@pytest.mark.django_db
def test_post_ordering(user):
    post1 = Post.objects.create(author=user, content="First post.")
    post2 = Post.objects.create(author=user, content="Second post.")

    posts = Post.objects.all()
    assert list(posts) == [post2, post1]


@pytest.mark.django_db
def test_post_author_relationship():
    user1 = Account.objects.create_user(username="user1", password="password123")
    user2 = Account.objects.create_user(username="user2", password="password123")

    post1 = Post.objects.create(author=user1, content="Post by user1.")
    post2 = Post.objects.create(author=user2, content="Post by user2.")

    assert post1.author == user1
    assert post2.author == user2
    assert post1.author != post2.author
