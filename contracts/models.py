import uuid
from django.db import models
from clients.models import Client
from vehicles.models import Vehicle
from django.core.exceptions import ValidationError


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
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Cliente")
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, verbose_name="Vehículo"
    )
    start_date = models.DateField("Inicio de contrato")
    weekly_payment = models.DecimalField(
        "Monto de cada cuota", max_digits=10, decimal_places=2
    )

    BILLING_CYCLE_CHOICES = [
        ("weekly", "Semanal"),
        ("biweekly", "Quincenal"),
        ("monthly", "Mensual"),
    ]
    billing_cycle = models.CharField(
        "Ciclo de facturación",
        max_length=10,
        choices=BILLING_CYCLE_CHOICES,
        default="weekly"
    )

    active = models.BooleanField("¿Está activo?", default=True)
    amount = models.DecimalField(
        "Valor total del contrato", max_digits=10, decimal_places=2, default=0
    )

    def clean(self):
        if self.active:
            existing = Contract.objects.filter(client=self.client, active=True)
            if self.pk:
                existing = existing.exclude(pk=self.pk)
            if existing.exists():
                raise ValidationError("Este cliente ya tiene un contrato activo.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Contrato #{self.id} — {self.client}"
