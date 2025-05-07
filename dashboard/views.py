from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from dashboard.utils.file_processor import process_excel_file, process_csv_file


class DashboardView(LoginRequiredMixin, TemplateView):
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
        return render(request, self.template_name)

    def post(self, request):
        """
        Handles POST requests for file uploads.

        Validates the uploaded file and returns appropriate error or success messages.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered dashboard page with error or success messages.
        """
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return render(
                request, self.template_name, {"error": "No se subió ningún archivo."}
            )

        if not uploaded_file.name.endswith((".csv", ".xlsx")):
            return render(
                request,
                self.template_name,
                {"error": "Formato no válido. Solo se permiten .csv o .xlsx"},
            )

        if uploaded_file.size > 5 * 1024 * 1024:
            # Lógica futura para procesamiento por lotes
            return render(
                request,
                self.template_name,
                {
                    "error": "El archivo supera los 5MB. Procesamiento por lotes no implementado aún."
                },
            )

        data = []

        if uploaded_file.name.endswith(".xlsx"):
            data, error = process_excel_file(uploaded_file)
        elif uploaded_file.name.endswith(".csv"):
            data, error = process_csv_file(uploaded_file)

        return render(
            request,
            self.template_name,
            {"data": data, "error": error},
        )
