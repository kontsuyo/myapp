from django.db import models


class Post(models.Model):
    author = models.ForeignKey("users.Account", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-posted_date"]

    def __str__(self):
        return f"Post by {self.author.username}"
