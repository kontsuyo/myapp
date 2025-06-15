from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post
from posts.permissions import IsAuthorOrReadOnly
from posts.serializers import (
    PostCreateSerializer,
    PostListSerializer,
    PostRetrieveSerializer,
)
from users.serializers import ProfileSerializer

User = get_user_model()


class PostHomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        posts = Post.objects.all().order_by("-posted_date")
        if not posts.exists():
            return Response({"detail": "No posts available."}, status=404)
        # ページネーションを適用
        paginator = PageNumberPagination()
        paginator.page_size = 20  # 1ページあたり20件（必要に応じて調整）
        page = paginator.paginate_queryset(posts, request)
        serializer = PostListSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response({"posts": serializer.data})


class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            post = serializer.save()
            return Response(
                {
                    "message": "Post created successfully.",
                    "post": {
                        "id": post.id,
                        "author": post.author.username,
                        "content": post.content,
                        "posted_date": post.posted_date.isoformat(),
                    },
                },
                status=201,
            )
        return Response(serializer.errors, status=400)


class PostListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"detail": "User not found."}, status=404)
        posts = Post.objects.filter(author=user)
        if not posts.exists():
            return Response({"detail": "No posts found for this user."}, status=404)
        posts_serializer = PostListSerializer(posts, many=True, context={"request": request})
        profile_serializer = ProfileSerializer(
            user.profile, context={"request": request}  # pyright: ignore[reportAttributeAccessIssue]
        )
        return Response({"posts": posts_serializer.data, "profile": profile_serializer.data}, status=200)


class PostRetrieveView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, username, post_id):
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"detail": "User not found."}, status=404)
        post = Post.objects.filter(id=post_id).first()
        if not post:
            return Response({"detail": "Post not found."}, status=404)
        serializer = PostRetrieveSerializer(post, context={"request": request})
        return Response(serializer.data, status=200)


class PostUpdateView(APIView):
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def patch(self, request, username, post_id):
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"detail": "User not found."}, status=404)
        post = Post.objects.filter(id=post_id, author=user).first()
        if not post:
            return Response({"detail": "Post not found."}, status=404)

        # オブジェクトパーミッションを明示的にチェック
        self.check_object_permissions(request, post)

        serializer = PostCreateSerializer(post, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            updated_post = serializer.save()
            return Response(
                {
                    "message": "Post updated successfully.",
                    "post": {
                        "id": updated_post.id,
                        "author": updated_post.author.username,
                        "content": updated_post.content,
                        "posted_date": updated_post.posted_date.isoformat(),
                    },
                },
                status=200,
            )
        return Response(serializer.errors, status=400)


class PostDeleteView(APIView):
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def delete(self, request, username, post_id):
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"detail": "User not found."}, status=404)
        post = Post.objects.filter(id=post_id, author=user).first()
        if not post:
            return Response({"detail": "Post not found."}, status=404)

        # APIViewのためオブジェクトパーミッションを明示的にチェック
        self.check_object_permissions(request, post)

        post.delete()
        return Response({"message": "Post deleted successfully."}, status=204)
