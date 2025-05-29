from django.urls import path

from users.views import (
    AccountDeleteView,
    AccoutUpdateView,
    LoginView,
    ProfileView,
    RegisterView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),  # !signupに変更
    path("login/", LoginView.as_view(), name="login"),
    path(
        "update_account/", AccoutUpdateView.as_view(), name="account-update"
    ),  # !update_accountに変更
    path("delete_account/", AccountDeleteView.as_view(), name="delete-account"),
    # path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    # path("update_profile/", UpdateProfileView.as_view(), name="update_profile"),
    # path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    # path("password_change/", PasswordChangeView.as_view(), name="password_change"),
]
