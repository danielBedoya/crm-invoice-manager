from .views import CreateInvoiceInstanceView
from django.urls import path

urlpatterns = [
    path("manage/", CreateInvoiceInstanceView.as_view(), name="manage_invoice"),
]