from django.urls import path

from .views import (
    AddToCartView,
    CartDetailView,
    RemoveCartItemView,
    UpdateCartItemView,
)

app_name = "cart"

urlpatterns = [
    path("", CartDetailView.as_view(), name="detail"),
    path("add/<int:variant_id>/", AddToCartView.as_view(), name="add"),
    path("update/<int:item_id>/", UpdateCartItemView.as_view(), name="update"),
    path("remove/<int:item_id>/", RemoveCartItemView.as_view(), name="remove"),
]