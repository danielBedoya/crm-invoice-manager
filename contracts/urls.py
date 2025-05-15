from .views import CreateContractInstanceView
from django.urls import path

urlpatterns = [
    path("manage/", CreateContractInstanceView.as_view(), name="manage_contract"),
]