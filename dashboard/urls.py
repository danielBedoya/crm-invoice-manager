from django.urls import path
from .views import DashboardView, RoleDashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("dashboard/user/", RoleDashboardView.as_view(), name="role_dashboard"),
]
