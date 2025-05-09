from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from .tasks import generate_and_send_report
from django.contrib import messages
import logging

logger = logging.getLogger('reports')


class ReportView(LoginRequiredMixin, View):
    """
    View for handling report generation requests.

    This view allows authenticated users to generate reports based on session data.
    The report generation is handled asynchronously using a background task.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to generate a report.

        This method retrieves data from the session, validates the presence of data,
        and sends a background task to generate the report. It notifies the user
        that the report will be sent via email.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: A response indicating the status of the report generation request.
        """
        try:
            user_email = request.user.email
            selected_columns = request.POST.getlist('columns')
            format = request.POST.get('format', 'csv')
            data = request.session.get("data", [])

            logger.info(f"Report request by {user_email} for columns: {selected_columns}")

            if not data:
                logger.info("No data found")
                return HttpResponse("No hay datos disponibles para generar el reporte.", status=400)

            generate_and_send_report.delay(user_email, selected_columns, data, format)

            messages.success(request, "Tu reporte está siendo procesado y será enviado a tu correo.")
            return redirect('dashboard')

        except Exception as e:
            logger.exception("Error while processing report request")
            messages.error(request, f"Ocurrió un error al procesar el reporte: {str(e)}")
            return redirect('dashboard')
