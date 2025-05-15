from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
import logging

from .models import Invoice

logger = logging.getLogger(__name__)


class CreateInvoiceInstanceView(LoginRequiredMixin, View):
    """
    View to handle the creation of a new Invoice instance via POST request.
    Inherits from:
        LoginRequiredMixin: Ensures the user is authenticated.
        View: Base Django class-based view.
    Methods:
        post(request):
            Processes POST data to create a new Invoice object, excluding the CSRF token.
            On success, adds a success message and redirects to the role dashboard.
            On failure, logs the exception, adds an error message, and redirects to the role dashboard.
    """

    def post(self, request):
        try:
            data = {k: v for k, v in request.POST.items() if k != "csrfmiddlewaretoken"}
            Invoice.objects.create(**data)
            messages.success(request, "Factura creada exitosamente.")
        except Exception as e:
            logger.error(f"Error creating invoice instance: {e}")
            messages.error(request, "Error al crear factura.")
        return redirect("role_dashboard")
