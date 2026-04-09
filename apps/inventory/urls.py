from django.urls import path

from .views import SellerInventoryManageView

app_name = "inventory"

urlpatterns = [
    path("seller/variant/<int:variant_id>/", SellerInventoryManageView.as_view(), name="seller_manage"),
]