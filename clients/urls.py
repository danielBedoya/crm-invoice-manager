from .views import CreateClientInstanceView
from django.urls import path

urlpatterns = [
    path("manage/", CreateClientInstanceView.as_view(), name="manage_client"),
]