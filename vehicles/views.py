from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
import logging

from vehicles.models import Vehicle, VehicleModel

logger = logging.getLogger(__name__)


class CreateVehicleInstanceView(LoginRequiredMixin, View):
    """
    View for creating and listing vehicle instances.
    Methods
    -------
    get(request):
        Returns a filtered list of vehicles based on query parameters.
        Filters are applied only for valid Vehicle model fields.
    post(request):
        Handles the creation of a new vehicle instance.
        Expects vehicle data in POST request, including a valid vehicle_model ID.
        On success, displays a success message and redirects to the role dashboard.
        On failure, logs the error and displays an error message.
    """

    def get(self, request):
        """
        Returns a filtered list of vehicles.
        """
        vehicles = Vehicle.objects.select_related("vehicle_model").all()
        filters = {
            k: v for k, v in request.GET.items()
            if k in [field.name for field in Vehicle._meta.fields]
        }
        if filters:
            vehicles = vehicles.filter(**filters)
        return vehicles

    def post(self, request):
        try:
            data = {k: v for k, v in request.POST.items() if k != "csrfmiddlewaretoken"}
            if "vehicle_model" in data:
                data["vehicle_model"] = VehicleModel.objects.get(pk=data["vehicle_model"])
            Vehicle.objects.create(**data)
            messages.success(request, "Vehículo creado exitosamente.")
        except Exception as e:
            logger.error(f"Error creating vehicle instance: {e}")
            messages.error(request, "Error al crear vehículo.")
        return redirect("role_dashboard")


class CreateVehicleModelInstanceView(LoginRequiredMixin, View):
    """
    View to handle the creation of a new VehicleModel instance via POST request.
    Inherits from:
        LoginRequiredMixin: Ensures the user is authenticated.
        View: Base Django class-based view.
    Methods:
        post(request):
            Processes POST data to create a new VehicleModel object, excluding the CSRF token.
            On success, adds a success message and redirects to the role dashboard.
            On failure, logs the exception, adds an error message, and redirects to the role dashboard.
    """

    def post(self, request):
        try:
            data = {k: v for k, v in request.POST.items() if k != "csrfmiddlewaretoken"}
            VehicleModel.objects.create(**data)
            messages.success(request, "Modelo de vehículo creado exitosamente.")
        except Exception as e:
            logger.error(f"Error creating vehicle model instance: {e}")
            messages.error(request, "Error al crear modelo de vehículo.")
        return redirect("role_dashboard")
