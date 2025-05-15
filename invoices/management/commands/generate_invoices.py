from django.core.management.base import BaseCommand
from django.utils.timezone import now
from invoices.models import Invoice, Contract
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Django management command to generate invoices for all active contracts that do not yet have an invoice for the current billing cycle.
    This command iterates through all active contracts and determines the current billing period key based on the contract's billing cycle (weekly, biweekly, or monthly).
    If an invoice for the current period does not already exist for a contract, a new invoice is created.
    Attributes:
        help (str): Description of the command for Django's help system.
    Methods:
        handle(*args, **options): Main entry point for the command. Generates invoices as needed and outputs the number of invoices created.
    """

    help = "Genera facturas para todos los contratos activos si aún no tienen una factura en el ciclo actual"

    def handle(self, *args, **options):
        try:
            today = now().date()
            generated_count = 0

            active_contracts = Contract.objects.filter(active=True)

            for contract in active_contracts:
                if contract.billing_cycle == "weekly":
                    year, week, _ = today.isocalendar()
                    current_period_key = f"{year}-W{week:02d}"
                elif contract.billing_cycle == "biweekly":
                    quincena = 1 if today.day <= 15 else 2
                    current_period_key = f"{today.year}-{today.month:02d}-Q{quincena}"
                else:  # monthly
                    current_period_key = f"{today.year}-{today.month:02d}"

                already_exists = Invoice.objects.filter(
                    contract=contract, period_key=current_period_key
                ).exists()

                if not already_exists:
                    Invoice.objects.create(
                        contract=contract,
                        issue_date=today,
                        due_date=today + timedelta(days=7),
                        amount=contract.amount,
                        period_key=current_period_key,
                    )
                    generated_count += 1

            self.stdout.write(
                self.style.SUCCESS(f"Generated Invoices: {generated_count}")
            )

        except Exception as e:
            logger.exception(f"Error generating invoices: {e}")
            self.stderr.write(self.style.ERROR(f"Error generating invoices: {str(e)}"))
