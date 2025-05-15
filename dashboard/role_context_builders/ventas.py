import logging
from django.test import RequestFactory
from clients.views import CreateClientInstanceView

logger = logging.getLogger(__name__)


def get_context(user):
    """
    Build and return the context dictionary for the 'ventas' dashboard role,
    based on the authenticated user.

    Args:
        user (User): Authenticated user object.

    Returns:
        dict: Context containing client data and permissions.
    """
    if not user.is_authenticated:
        return {}

    # Create a fake GET request to retrieve clients from the view
    factory = RequestFactory()
    fake_request = factory.get("/fake-url")
    fake_request.user = user

    clients_qs = CreateClientInstanceView().get(fake_request)

    clients_list = []
    for client in clients_qs:
        active_contract = client.contract_set.filter(active=True).first()
        clients_list.append(
            {
                "full_name": f"{client.first_name} {client.last_name}",
                "document_number": client.document_number,
                "active_contract": "Si" if active_contract is not None else "No",
                "linked_vehicle": (
                    str(active_contract.vehicle) if active_contract else "No tiene contrato activo"
                ),
            }
        )

    context = {
        "headers": {
            "values": clients_list[0].keys() if clients_list else [],
            "labels": {
                "full_name": "Nombre completo",
                "document_number": "Número de documento",
                "active_contract": "Contrato activo",
                "linked_vehicle": "Vehículo vinculado",
            },
        },
        "rows": clients_list,
        "pagination": 20,
    }

    return context
