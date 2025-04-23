from django.contrib.auth.models import AbstractUser


class UserAccount(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """

    pass

    def __str__(self):
        return self.username
