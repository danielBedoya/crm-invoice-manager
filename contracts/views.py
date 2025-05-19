from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Prefetch
import logging

from .models import Contract
from clients.models import Client
from vehicles.models import Vehicle
from invoices.models import Invoice

logger = logging.getLogger(__name__)


class CreateContractInstanceView(LoginRequiredMixin, View):
    """
    View to handle the creation of a new Contract instance via POST request.

    Inherits from:
        LoginRequiredMixin: Ensures the user is authenticated.
        View: Base Django class-based view.

    Methods:
        post(request):
            Processes POST data to create a new Contract object, excluding the CSRF token.
            On success, adds a success message and redirects to the role dashboard.
            On failure, logs the exception, adds an error message, and redirects to the role dashboard.
    """

    def post(self, request):
        try:
            data = {k: v for k, v in request.POST.items() if k != "csrfmiddlewaretoken"}

            if "client" in data:
                client = Client.objects.get(pk=data["client"])
                if client.contract_set.filter(active=True).exists():
                    messages.error(request, "El cliente ya tiene un contrato activo.")
                    return redirect("role_dashboard")
                data["client"] = client

            if "vehicle" in data:
                vehicle = Vehicle.objects.get(pk=data["vehicle"])
                if vehicle.contract_set.filter(active=True).exists():
                    messages.error(request, "El vehículo ya tiene un contrato activo.")
                    return redirect("role_dashboard")
                data["vehicle"] = vehicle

            if "active" in data:
                data["active"] = bool(data["active"])

            Contract.objects.create(**data)
            messages.success(request, "Contrato creado exitosamente.")
        except Exception as e:
            logger.error(f"Error creating contract instance: {e}")
            messages.error(request, "Error al crear contrato.")
        return redirect("role_dashboard")


class DashboardContractListView(LoginRequiredMixin, ListView):
    model = Contract
    template_name = None
    context_object_name = "contracts"
    paginate_by = 20

    def get_queryset(self):
        try:
            filter_params = {k: v for k, v in self.request.GET.items() if v}

            logger.debug(
                f"[DashboardContractListView] Filtros dinámicos: {filter_params}"
            )

            return (
                Contract.objects
                .filter(**filter_params)
                .select_related("client", "vehicle", "vehicle__vehicle_model")
                .prefetch_related(
                    Prefetch(
                        "invoice_set",
                        queryset=Invoice.objects.filter(payment_status="pagado"),
                        to_attr="paid_invoices",
                    ),
                )
            )
        except Exception as e:
            logger.error(f"[DashboardContractListView] Error al aplicar filtros: {e}")
            return Contract.objects.none()
