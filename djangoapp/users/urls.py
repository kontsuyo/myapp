from django.urls import path

from users.views import (
    AccountDeleteView,
    AccoutUpdateView,
    LoginView,
    ProfileView,
    RegisterView,
)

urlpatterns = [
    path("signup/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("update_account/", AccoutUpdateView.as_view(), name="update-account"),
    path("delete_account/", AccountDeleteView.as_view(), name="delete-account"),
    path("profile/", ProfileView.as_view(), name="profile"),
    # path("logout/", LogoutView.as_view(), name="logout"),
    # path("update_profile/", UpdateProfileView.as_view(), name="update_profile"),
    # path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    # path("password_change/", PasswordChangeView.as_view(), name="password_change"),
]
