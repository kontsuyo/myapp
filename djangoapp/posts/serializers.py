from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Post
        fields = ["author", "content", "posted_date"]
        read_only_fields = ["posted_date"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["author"] = user
        post = Post.objects.create(**validated_data)
        return post
