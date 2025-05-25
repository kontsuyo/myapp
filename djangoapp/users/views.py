from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import (
    AccountUpdateSerializer,
    LoginSerializer,
    RegisterSerializer,
)

User = get_user_model()


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "ユーザー登録が完了しました。"}, status=201)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=serializer.validated_data["username"])  # type: ignore
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "message": "ログインに成功しました。",
                    "token": token.key,
                    "username": user.username,
                },
                status=200,
            )
        return Response(serializer.errors, status=400)


class AccoutUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def patch(self, request):
        serializer = AccountUpdateSerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=request.user.username)
            user.username = serializer.validated_data["username"]  # type: ignore
            user.save()
            return Response(
                {
                    "message": "ユーザー情報が更新されました。",
                    "username": user.username,
                },
                status=200,
            )
        return Response(serializer.errors, status=400)


class AccountDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def delete(self, request):
        user = User.objects.get(username=request.user.username)
        user.delete()
        return Response({"message": "ユーザーが削除されました。"}, status=200)
