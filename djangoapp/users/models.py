from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


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
