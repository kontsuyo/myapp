from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Post
        fields = ["id", "author", "content", "posted_date"]
        read_only_fields = ["posted_date"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["author"] = user
        post = Post.objects.create(**validated_data)
        return post


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["content"]
        read_only_fields = ["author", "posted_date"]

    def validate(self, attrs):
        instance = self.instance
        if instance and timezone.now() - instance.posted_date > timedelta(minutes=30):
            raise serializers.ValidationError({"content": ["投稿の編集は投稿後30分以内のみ可能です。"]})
        return attrs

    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance
