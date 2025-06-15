import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from users.models import Account

User = get_user_model()


@pytest.fixture
def api_client():
    yield APIClient()


@pytest.fixture
def user_data():
    """
    Fixture to provide user data for testing.
    """
    return {
        "username": "testuser",
        "password": "testpassword",
        "password_confirm": "testpassword",
    }


@pytest.fixture
def user():
    return Account.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def profile_data():
    return {
        "handle": "Test User",
        "bio": "This is a test bio.",
        "profile_image": None,  # Assuming no image for simplicity
        "place": "Test Place",
        "website": "https://testuser.com",
    }
