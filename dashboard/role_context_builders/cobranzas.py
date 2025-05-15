import logging
import math
from django.test import RequestFactory
from django.utils.timezone import now
from contracts.views import DashboardContractListView

logger = logging.getLogger(__name__)

def get_context(user):
    """
    Builds and returns the context dictionary for the dashboard contract list view for a given user.
    Args:
        user (User): The user object for whom the context is being built.
    Returns:
        dict: A context dictionary containing:
            - 'headers': A dictionary with 'values' (list of column keys) and 'labels' (mapping of keys to display names).
            - 'rows': A list of dictionaries, each representing a contract with client and vehicle information, payment details, and pending installments.
            - 'pagination': The number of items per page for pagination.
    Notes:
        - If the user is not authenticated, returns an empty dictionary.
        - Calculates the number of pending installments based on the total contract amount, paid invoices, and weekly payment.
        - Handles contracts without associated vehicles and contracts with zero weekly payment.
    """
    
    if not user.is_authenticated:
        return {}

    factory = RequestFactory()
    request = factory.get("/fake-url")
    request.user = user

    view = DashboardContractListView()
    view.request = request
    contracts = view.get_queryset()

    rows = []
    for contract in contracts:
        client = contract.client
        vehicle = contract.vehicle
        row = {
            "full_name": f"{client.first_name} {client.last_name}",
            "billing_cycle": contract.billing_cycle,
            "weekly_payment": contract.weekly_payment,
            "document_number": client.document_number,
            "amount": contract.amount,
            "active": "Si" if contract.active else "No",
            "vehicle_info": str(vehicle) if vehicle else "Sin vehículo"
        }
        paid_invoices = contract.invoice_set.filter(payment_status="pagado")
        total_paid = sum(invoice.amount for invoice in paid_invoices)
        remaining_amount = max(contract.amount - total_paid, 0)
        pending_installments = math.ceil(remaining_amount / contract.weekly_payment) if contract.weekly_payment else 0
        row["pending_installments"] = pending_installments
        rows.append(row)

    headers = {
        "values": ["full_name", "document_number", "active", "vehicle_info", "pending_installments", "billing_cycle", "weekly_payment", "amount"],
        "labels": {
            "full_name": "Nombre completo",
            "document_number": "Número de documento",
            "active": "¿Esta Activo?",
            "vehicle_info": "Vehículo asociado",
            "pending_installments": "Cuotas pendientes",
            "billing_cycle": "Ciclo de facturación",
            "weekly_payment": "Cuota",
            "amount": "Monto total",
        },
    }

    context = {
        "headers": headers,
        "rows": rows,
        "pagination": 20,
    }

    return context
