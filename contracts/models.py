from django.db import models
from clients.models import Client
from vehicles.models import Vehicle


class Contract(models.Model):
    """
    Model representing a contract.

    This model stores information about a contract between a client and a vehicle,
    including the start date, weekly payment amount, and contract status.

    Attributes:
        client (ForeignKey): A reference to the associated client (Client model).
        vehicle (ForeignKey): A reference to the associated vehicle (Vehicle model).
        start_date (DateField): The start date of the contract.
        weekly_payment (DecimalField): The weekly payment amount for the contract.
        status (CharField): The status of the contract, with choices:
            - "activo": Active contract.
            - "cancelado": Canceled contract.
            - "finalizado": Completed contract.

    Methods:
        __str__(): Returns a string representation of the contract, including its ID and associated client.
    """

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Cliente")
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, verbose_name="Vehículo"
    )
    start_date = models.DateField("Inicio de contrato")
    weekly_payment = models.DecimalField(
        "Cuota semanal", max_digits=10, decimal_places=2
    )

    STATUS_CHOICES = [
        ("activo", "Activo"),
        ("cancelado", "Cancelado"),
        ("finalizado", "Finalizado"),
    ]
    status = models.CharField(
        "Estado", max_length=20, choices=STATUS_CHOICES, default="activo"
    )

    def __str__(self):
        return f"Contrato #{self.id} — {self.client}"
