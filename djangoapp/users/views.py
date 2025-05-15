from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import RegisterSerializer

User = get_user_model()


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "ユーザー登録が完了しました。"}, status=201)
        return Response(serializer.errors, status=400)
