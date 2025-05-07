from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.

    This model uses email as the unique identifier for authentication
    instead of the default username field.

    Attributes:
        email (EmailField): The user's email address, which must be unique.
        USERNAME_FIELD (str): Specifies the field to be used as the unique identifier.
        REQUIRED_FIELDS (list): Specifies the required fields other than the USERNAME_FIELD.
    """

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
