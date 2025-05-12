from django.urls import path
from .views import ReportView

urlpatterns = [
    path("generar-reporte/", ReportView.as_view(), name="generate_report"),
]
