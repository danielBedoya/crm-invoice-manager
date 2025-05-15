import uuid
from django.db import models
from contracts.models import Contract


class Invoice(models.Model):
    """
    Model representing an invoice.

    This model stores information about an invoice associated with a contract,
    including issue date, due date, amount, and payment status.

    Attributes:
        uid (UUIDField): A unique identifier for the invoice (auto-generated).
        contract (ForeignKey): A reference to the associated contract (Contract model).
        issue_date (DateField): The date the invoice was issued.
        due_date (DateField): The due date for the invoice payment.
        amount (DecimalField): The total amount of the invoice.
        payment_status (CharField): The payment status of the invoice, with choices:
            - "pendiente": Pending payment.
            - "pagado": Paid.
            - "vencido": Overdue.

    Methods:
        __str__(): Returns a string representation of the invoice, including its ID and associated contract.
    """

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, verbose_name="Contrato"
    )
    issue_date = models.DateField("Fecha de emisión")
    due_date = models.DateField("Fecha de vencimiento")
    amount = models.DecimalField("Valor", max_digits=10, decimal_places=2)

    PAYMENT_STATUS_CHOICES = [
        ("pendiente", "Pendiente"),
        ("pagado", "Pagado"),
        ("vencido", "Vencido"),
    ]
    payment_status = models.CharField(
        "Estado de pago",
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pendiente",
    )
    period_key = models.CharField(
        "Periodo de facturación", max_length=20, blank=True, null=True
    )

    def __str__(self):
        return f"Factura #{self.id} — {self.contract}"
