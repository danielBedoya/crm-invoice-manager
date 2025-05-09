from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
import logging

from dashboard.utils.file_processor import process_excel_file, process_csv_file
from dashboard.utils.search_utils import filter_data

logger = logging.getLogger("dashboard")


class DashboardView(LoginRequiredMixin, View):
    """
    Main dashboard view for authenticated users.

    This view displays the dashboard and requires the user
    to be authenticated to access it.

    Attributes:
        template_name (str): Path to the template used for the dashboard page.
    """

    template_name = "dashboard/dashboard.html"

    def get(self, request):
        """
        Handles GET requests and renders the dashboard page.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered dashboard page.
        """
        try:
            q = request.GET.get("q")
            data = request.session.get("data", [])

            if q:
                logger.info(f"Search query received: '{q}'")
                data = filter_data(data, q)

            if data:
                paginator = Paginator(data, 20)
                page_number = request.GET.get("page", 1)
                logger.info(f"Paginating dashboard data. Page: {page_number}")
                page_obj = paginator.get_page(page_number)
                return render(
                    request, self.template_name, {"page_obj": page_obj, "q": q}
                )

            logger.info("No data available in session for dashboard.")
            return render(request, self.template_name)

        except Exception as e:
            logger.exception("Unexpected error during GET request to dashboard")
            return render(
                request,
                self.template_name,
                {
                    "error": f"Ocurrió un error inesperado al cargar el dashboard: {str(e)}"
                },
            )

    def post(self, request):
        """
        Handles POST requests for file uploads.

        Validates the uploaded file and returns appropriate error or success messages.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered dashboard page with error or success messages.
        """
        try:
            uploaded_file = request.FILES.get("file")
            if not uploaded_file:
                logger.warning("No file was uploaded.")
                return render(
                    request,
                    self.template_name,
                    {"error": "No se subió ningún archivo."},
                )

            if not uploaded_file.name.endswith((".csv", ".xlsx")):
                logger.warning(f"Unsupported file type uploaded: {uploaded_file.name}")
                return render(
                    request,
                    self.template_name,
                    {"error": "Formato no válido. Solo se permiten .csv o .xlsx"},
                )

            if uploaded_file.size > 5 * 1024 * 1024:
                logger.warning(f"File exceeds 5MB: {uploaded_file.name}")
                return render(
                    request,
                    self.template_name,
                    {
                        "error": "El archivo supera los 5MB. Procesamiento por lotes no implementado aún."
                    },
                )

            logger.info(f"Processing uploaded file: {uploaded_file.name}")

            if uploaded_file.name.endswith(".xlsx"):
                data, error = process_excel_file(uploaded_file)
            elif uploaded_file.name.endswith(".csv"):
                data, error = process_csv_file(uploaded_file)

            if error:
                logger.error(f"File processing error: {error}")
                return render(request, self.template_name, {"error": error})

            request.session["data"] = data
            paginator = Paginator(data, 20)
            page_number = request.GET.get("page", 1)
            page_obj = paginator.get_page(page_number)

            return render(request, self.template_name, {"page_obj": page_obj})

        except Exception as e:
            logger.exception("Unexpected error during file upload")
            return render(
                request,
                self.template_name,
                {
                    "error": f"Ocurrió un error inesperado al procesar el archivo: {str(e)}"
                },
            )
