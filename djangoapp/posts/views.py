from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post
from posts.serializers import PostSerializer

User = get_user_model()


class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={"request": request})
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
        if not user.posts.exists():  # pyright: ignore[reportAttributeAccessIssue]
            return Response({"detail": "No posts found for this user."}, status=404)
        posts = user.posts.all()  # pyright: ignore[reportAttributeAccessIssue]
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data, status=200)


class PostRetrieveView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, username, post_id):
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"detail": "User not found."}, status=404)
        post = Post.objects.filter(id=post_id).first()
        if not post:
            return Response({"detail": "Post not found."}, status=404)
        serializer = PostSerializer(post, context={"request": request})
        return Response(serializer.data, status=200)
