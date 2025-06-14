from django.urls import path

from posts.views import PostCreateView, PostListView, PostRetrieveView, PostUpdateView

urlpatterns = [
    path("", PostCreateView.as_view(), name="post"),
    path("<slug:username>/", PostListView.as_view(), name="post-list"),
    path("<slug:username>/<int:post_id>", PostRetrieveView.as_view(), name="post-detail"),
    path("<slug:username>/update/<int:post_id>", PostUpdateView.as_view(), name="post-update"),
]
