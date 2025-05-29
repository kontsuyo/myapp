import logging

import pytest

from users.models import Account

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_signal_profile_creation_on_user_save():
    user = Account.objects.create_user(username="testuser", password="testpassword")
    assert hasattr(user, "profile")
    assert user.profile.handle == ""  # pyright:ignore[reportAttributeAccessIssue]
    assert user.profile.bio == ""  # pyright:ignore[reportAttributeAccessIssue]
    assert user.profile.place == ""  # pyright:ignore[reportAttributeAccessIssue]
    assert not user.profile.profile_image  # pyright:ignore[reportAttributeAccessIssue]


@pytest.mark.django_db
def test_signal_profile_update_on_user_save():
    user = Account.objects.create_user(username="testuser", password="testpassword")
    user.username = "updateduser"
    user.profile.handle = "Updated Handle"  # pyright:ignore[reportAttributeAccessIssue]
    user.profile.bio = "Updated bio."  # pyright:ignore[reportAttributeAccessIssue]
    user.profile.place = "Updated Place"  # pyright:ignore[reportAttributeAccessIssue]
    user.save()

    # Check if the profile is updated correctly
    assert user.profile.handle == "Updated Handle"  # pyright:ignore[reportAttributeAccessIssue]
    assert user.profile.bio == "Updated bio."  # pyright:ignore[reportAttributeAccessIssue]
    assert user.profile.place == "Updated Place"  # pyright:ignore[reportAttributeAccessIssue]
    assert not user.profile.profile_image  # pyright:ignore[reportAttributeAccessIssue]
    assert user.username == "updateduser"
