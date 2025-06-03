from django.urls import path

from posts.views import PostCreateView

urlpatterns = [
    path("", PostCreateView.as_view(), name="post"),
]
