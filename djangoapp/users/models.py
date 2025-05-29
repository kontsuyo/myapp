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


class Profile(models.Model):
    user = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="ユーザー",
    )
    handle = models.CharField(
        blank=True,
        max_length=50,
        verbose_name="ハンドルネーム",
    )
    bio = models.TextField(
        blank=True,
        max_length=160,
        verbose_name="自己紹介",
    )
    profile_image = models.ImageField(
        blank=True,
        null=True,
        upload_to="profile_images/",
        verbose_name="プロフィール画像",
    )
    place = models.CharField(
        blank=True,
        max_length=30,
        verbose_name="場所",
    )
    website = models.URLField(
        blank=True,
        max_length=100,
        verbose_name="ウェブサイト",
    )

    def __str__(self):
        return f"{self.user.username} Profile"
