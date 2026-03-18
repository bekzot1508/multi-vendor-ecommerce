from django.urls import path

from .views import (
    ProductDetailView,
    SellerProductCreateView,
    SellerProductDeleteView,
    SellerProductListView,
    SellerProductUpdateView,
)

app_name = "catalog"

urlpatterns = [
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),

    path("seller/products/", SellerProductListView.as_view(), name="seller_product_list"),
    path("seller/products/create/", SellerProductCreateView.as_view(), name="seller_product_create"),
    path("seller/products/<int:pk>/edit/", SellerProductUpdateView.as_view(), name="seller_product_edit"),
    path("seller/products/<int:pk>/delete/", SellerProductDeleteView.as_view(), name="seller_product_delete"),
]