from django.urls import path

from users.views import LoginView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),  # !signupに変更
    path("login", LoginView.as_view(), name="login"),
    # path("logout/", LogoutView.as_view(), name="logout"),
    # path("profile/", UserProfileView.as_view(), name="profile"),
    # path("update_profile/", UpdateProfileView.as_view(), name="update_profile"),
    # path("delete_account/", DeleteAccountView.as_view(), name="delete_account"),
    # path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    # path("password_change/", PasswordChangeView.as_view(), name="password_change"),
]
