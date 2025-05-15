from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
import logging

from .models import Client

logger = logging.getLogger(__name__)


class CreateClientInstanceView(LoginRequiredMixin, View):
    """
    View to handle the creation of a new Client instance via POST request.
    Inherits from:
        LoginRequiredMixin: Ensures the user is authenticated.
        View: Base Django class-based view.
    Methods:
        post(request):
            Processes POST data to create a new Client object, excluding the CSRF token.
            On success, adds a success message and redirects to the role dashboard.
            On failure, logs the exception, adds an error message, and redirects to the role dashboard.
    """
    def post(self, request):
        try:
            data = {k: v for k, v in request.POST.items() if k != "csrfmiddlewaretoken"}
            Client.objects.create(**data)
            messages.success(request, "Cliente creado exitosamente.")
        except Exception as e:
            logger.error(f"Error creating client instance: {e}")
            messages.error(request, "Error al crear cliente.")
        return redirect("role_dashboard")

    def get(self, request):
        """
        Handles GET requests to retrieve a queryset of Client objects, optionally filtered by query parameters.
        Retrieves all Client instances from the database, prefetching related contracts and vehicles for efficiency.
        Applies filtering based on query parameters that match Client model fields.
        Returns the filtered queryset of clients. In case of an exception, logs the error and returns an empty queryset.
        Args:
            request (HttpRequest): The HTTP request object containing optional query parameters for filtering.
        Returns:
            QuerySet: A queryset of Client objects, filtered according to the request parameters, or an empty queryset on error.
        """
        
        try:
            clientes = Client.objects.all().prefetch_related('contract_set__vehicle')

            filters = {k: v for k, v in request.GET.items() if k in [field.name for field in Client._meta.fields]}
            if filters:
                clientes = clientes.filter(**filters)

            return clientes
        except Exception as e:
            logger.error(f"Error retrieving client list: {e}")
            return Client.objects.none()