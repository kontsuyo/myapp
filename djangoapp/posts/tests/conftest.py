import pytest

from users.models import Account


@pytest.fixture
def user():
    return Account.objects.create_user(
        username="testuser",
        password="testpassword",
    )
