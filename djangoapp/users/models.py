from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """

    username = models.SlugField(
        blank=False,
        max_length=15,
        unique=True,
        verbose_name="ユーザー名",
    )
    password = models.CharField(blank=False, max_length=128, verbose_name="パスワード")

    def __str__(self):
        return self.username
