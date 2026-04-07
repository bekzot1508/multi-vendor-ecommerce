from django.urls import path

from .views import (
    SellerShipmentDetailView,
    SellerShipmentStatusUpdateView,
    ShipmentDetailView,
)

app_name = "shipping"

urlpatterns = [
    path("<int:shipment_id>/", ShipmentDetailView.as_view(), name="detail"),
    path("seller/<int:shipment_id>/", SellerShipmentDetailView.as_view(), name="seller_detail"),
    path("seller/<int:shipment_id>/status/", SellerShipmentStatusUpdateView.as_view(), name="seller_status"),
]