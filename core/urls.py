from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("dashboard.urls")),
    path("", include("reports.urls")),
    path("invoices/", include("invoices.urls")),
    path("contracts/", include("contracts.urls")),
    path("vehicles/", include("vehicles.urls")),
    path("clients/", include("clients.urls")),
    path("django-rq/", include("django_rq.urls")),
]
