import pytest
from rest_framework.test import APIClient

from users.models import Account


@pytest.fixture
def user():
    return Account.objects.create_user(
        username="testuser",
        password="testpassword",
    )


@pytest.fixture
def api_client():
    return APIClient()
