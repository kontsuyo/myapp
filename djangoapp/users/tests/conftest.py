import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

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
    """
    Fixture to create a user for testing.
    """
    user = User.objects.create_user(username="testuser", password="testpassword")
    return user


@pytest.fixture
def profile_data():
    return {
        "handle": "Test User",
        "bio": "This is a test bio.",
        "profile_image": None,  # Assuming no image for simplicity
        "place": "Test Place",
        "website": "https://testuser.com",
    }
