import re

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import Profile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(
        max_length=15,
        error_messages={
            "max_length": "ユーザー名は15文字までにしてください。",
            "blank": "ユーザー名を入力してください。",
        },
    )
    password = serializers.CharField(
        write_only=True,
        error_messages={"blank": "パスワードを入力してください。"},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        error_messages={"blank": "確認用パスワードを入力してください。"},
    )

    class Meta:
        model = User
        fields = ["username", "password", "password_confirm"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "ユーザー名は使われています。他のものを選んでください"
            )
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise serializers.ValidationError(
                "ユーザー名は英数字と'_'(アンダーバー)が使えます"
            )
        if not 4 <= len(value):
            raise serializers.ValidationError("ユーザー名は4文字以上にしてください。")
        return value

    def validate_password(self, value):
        if not 8 <= len(value):
            raise serializers.ValidationError(
                "8文字以上のパスワードを入力してください。"
            )
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("パスワードが間違っています。")
        validate_password(attrs["password"])
        attrs.pop("password_confirm")
        return attrs

    def create(self, validated_data):
        user = User(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.SlugField(
        write_only=True,
        error_messages={
            "blank": "ユーザー名を入力してください。",
            "invalid": "ユーザー名が正しくありません。",
        },
    )
    password = serializers.CharField(
        write_only=True,
        error_messages={"blank": "パスワードを入力してください。"},
    )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = User.objects.filter(username=username).first()
        if user is None:
            raise serializers.ValidationError(
                {"username": "ユーザー名が正しくありません。"}
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                {"password": "パスワードが正しくありません。"}
            )

        return attrs


class AccountUpdateSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(
        max_length=15,
        error_messages={
            "max_length": "ユーザー名は15文字までにしてください。",
            "blank": "ユーザー名を入力してください。",
            "invalid": "ユーザー名は英数字と'_'(アンダーバー)が使えます",
        },
    )

    class Meta:
        model = User
        fields = ["username"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "ユーザー名は使われています。他のものを選んでください"
            )
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise serializers.ValidationError(
                "ユーザー名は英数字と'_'(アンダーバー)が使えます"
            )
        if not 4 <= len(value):
            raise serializers.ValidationError("ユーザー名は4文字以上にしてください。")
        return value

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]
        read_only_fields = ["username"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["user", "handle", "bio", "profile_image", "place", "website"]
