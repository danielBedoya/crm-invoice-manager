from .views import CreateVehicleInstanceView, CreateVehicleModelInstanceView
from django.urls import path

urlpatterns = [
    path("manage/", CreateVehicleInstanceView.as_view(), name="manage_vehicle"),
    path("manage/model/", CreateVehicleModelInstanceView.as_view(), name="manage_vehiclemodel"),
]