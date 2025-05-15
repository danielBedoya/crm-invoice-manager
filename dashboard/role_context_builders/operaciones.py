import logging
from django.test import RequestFactory
from django.utils.timezone import now
from vehicles.views import CreateVehicleInstanceView

logger = logging.getLogger(__name__)


def get_context(user):
    """
    Builds a context dictionary containing vehicle and contract information for a given authenticated user.
    This function simulates a request to retrieve a list of vehicles associated with the user,
    then constructs a list of dictionaries (rows) with details about each vehicle, including:
    - Brand and model
    - License plate
    - Whether there is an active contract
    - The end date of the last finalized contract's invoice (if any)
    - The number of days since the last contract ended
    The context also includes table headers and pagination information.
    Args:
        user (User): The user for whom the context is being built. Must have an 'is_authenticated' attribute.
    Returns:
        dict: A context dictionary with the following keys:
            - 'headers': Table headers and labels for display.
            - 'rows': List of dictionaries with vehicle and contract details.
            - 'pagination': Number of rows per page (default: 20).
            Returns an empty dictionary if the user is not authenticated.
    """

    if not user.is_authenticated:
        return {}

    # Fake request to reuse the vehicle listing view
    factory = RequestFactory()
    request = factory.get("/fake-url")
    request.user = user

    vehicles = CreateVehicleInstanceView().get(request)

    rows = []
    for vehicle in vehicles:
        last_contract_end = ""
        days_since_last_contract = "N/A"
        active_contract = vehicle.contract_set.filter(active=True).first()
        if not active_contract:
            last_contract_ended = (
                vehicle.contract_set.filter(active=False)
                .order_by("-start_date")
                .first()
                or "N/A"
            )
            if last_contract_ended and last_contract_ended != "N/A":
                last_invoice = last_contract_ended.invoices.order_by(
                    "-issued_date"
                ).first()
                last_contract_end = last_invoice.issued_date if last_invoice else ""
                days_since_last_contract = (
                    (now().date() - last_contract_end).days
                    if last_contract_end
                    else "N/A"
                )
        row = {
            "brand": vehicle.vehicle_model.brand if vehicle.vehicle_model else None,
            "model": vehicle.vehicle_model.model if vehicle.vehicle_model else None,
            "plate": vehicle.license_plate,
            "active_contract": bool(active_contract),
            "last_contract_end": last_contract_end,
            "days_since_last_contract": days_since_last_contract,
        }

        rows.append(row)

    headers = {
        "values": [
            "brand",
            "model",
            "plate",
            "active_contract",
            "last_contract_end",
            "days_since_last_contract",
        ],
        "labels": {
            "brand": "Marca",
            "model": "Modelo",
            "plate": "Placa",
            "active_contract": "Contrato activo",
            "last_contract_end": "Fin del último contrato",
            "days_since_last_contract": "Días sin contrato",
        },
    }

    context = {"headers": headers, "rows": rows, "pagination": 20}

    return context
