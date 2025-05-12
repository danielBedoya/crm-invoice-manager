import json
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField


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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.email


class FieldPermission(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="field_permissions")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    allowed_fields = models.TextField(default="[]", blank=True)

    def get_allowed_fields(self):
        try:
            return json.loads(self.allowed_fields)
        except (ValueError, TypeError):
            return []

    def set_allowed_fields(self, fields_list):
        self.allowed_fields = json.dumps(fields_list)

    class Meta:
        unique_together = ("group", "content_type")
        verbose_name = "Permiso por campo"
        verbose_name_plural = "Permisos por campo"

    def __str__(self):
        fields = ", ".join(self.get_allowed_fields())
        return f"{self.group.name} puede ver [{fields}] de {self.content_type.app_label}.{self.content_type.model}"
