from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 安全なメソッド(GET等)は許可
        if request.method in permissions.SAFE_METHODS:
            return True
        # 投稿者のみ編集可
        return obj.author == request.user
