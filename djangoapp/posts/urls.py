from django.urls import path

from posts.views import (
    PostCreateView,
    PostDeleteView,
    PostListView,
    PostRetrieveView,
    PostUpdateView,
)

urlpatterns = [
    path("post", PostCreateView.as_view(), name="post"),
    path("<slug:username>/", PostListView.as_view(), name="post-list"),
    path("<slug:username>/<int:post_id>", PostRetrieveView.as_view(), name="post-detail"),
    path("<slug:username>/update/<int:post_id>", PostUpdateView.as_view(), name="post-update"),
    path("<slug:username>/delete/<int:post_id>", PostDeleteView.as_view(), name="post-delete"),
]
