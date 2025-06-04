from django.urls import path

from posts.views import PostCreateView, PostDetailView, PostListView

urlpatterns = [
    path("", PostCreateView.as_view(), name="post"),
    path("<slug:username>/", PostListView.as_view(), name="post-list"),
    path("<slug:username>/post/<int:post_id>", PostDetailView.as_view(), name="post-detail"),
]
