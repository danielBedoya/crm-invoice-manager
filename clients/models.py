import uuid
from django.db import models


class Client(models.Model):
    """
    Model representing a client.

    This model stores information about a client, including their personal
    details and contact information.

    Attributes:
        uid (UUIDField): A unique identifier for the client (auto-generated).
        first_name (CharField): The first name of the client (max length: 100).
        last_name (CharField): The last name of the client (max length: 100).
        document_number (CharField): A unique identifier for the client (e.g., ID or document number, max length: 30).
        phone (CharField): The client's phone number (optional, max length: 20).
        email (EmailField): The client's unique email address.

    Methods:
        __str__(): Returns the full name of the client as a string.
    """

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField("Nombres", max_length=100)
    last_name = models.CharField("Apellidos", max_length=100)
    document_number = models.CharField(
        "Número de documento", max_length=30, unique=True
    )
    phone = models.CharField("Teléfono", max_length=20, blank=True)
    email = models.EmailField("Correo electrónico", unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
