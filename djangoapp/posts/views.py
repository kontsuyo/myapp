from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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
