from django.urls import path

from posts.views import PostCreateView, PostListView

urlpatterns = [
    path("", PostCreateView.as_view(), name="post"),
    path("<slug:username>/", PostListView.as_view(), name="post-list"),
]
