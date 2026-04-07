from django.urls import path

from .views import (
    CheckoutView,
    OrderDetailView,
    OrderListView,
    SellerOrderItemDetailView,
    SellerOrderItemListView,
    SellerOrderItemStatusUpdateView,
)

app_name = "orders"

urlpatterns = [
    path("", OrderListView.as_view(), name="list"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("<int:order_id>/", OrderDetailView.as_view(), name="detail"),

    path("seller/items/", SellerOrderItemListView.as_view(), name="seller_item_list"),
    path("seller/items/<int:item_id>/", SellerOrderItemDetailView.as_view(), name="seller_item_detail"),
    path("seller/items/<int:item_id>/status/", SellerOrderItemStatusUpdateView.as_view(), name="seller_item_status"),
]