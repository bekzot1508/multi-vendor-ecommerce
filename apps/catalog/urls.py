from django.urls import path

from .views import (
    ProductDetailView,
    SellerImageCreateView,
    SellerImageDeleteView,
    SellerProductCreateView,
    SellerProductDeleteView,
    SellerProductListView,
    SellerProductManageView,
    SellerProductUpdateView,
    SellerVariantCreateView,
    SellerVariantDeleteView,
    SellerVariantUpdateView,
)

app_name = "catalog"

urlpatterns = [
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),

    path("seller/products/", SellerProductListView.as_view(), name="seller_product_list"),
    path("seller/products/create/", SellerProductCreateView.as_view(), name="seller_product_create"),
    path("seller/products/<int:pk>/edit/", SellerProductUpdateView.as_view(), name="seller_product_edit"),
    path("seller/products/<int:pk>/delete/", SellerProductDeleteView.as_view(), name="seller_product_delete"),

    path("seller/products/<int:pk>/manage/", SellerProductManageView.as_view(), name="seller_product_manage"),

    path("seller/products/<int:product_id>/variants/create/", SellerVariantCreateView.as_view(), name="seller_variant_create"),
    path("seller/variants/<int:variant_id>/edit/", SellerVariantUpdateView.as_view(), name="seller_variant_edit"),
    path("seller/variants/<int:variant_id>/delete/", SellerVariantDeleteView.as_view(), name="seller_variant_delete"),

    path("seller/products/<int:product_id>/images/create/", SellerImageCreateView.as_view(), name="seller_image_create"),
    path("seller/images/<int:image_id>/delete/", SellerImageDeleteView.as_view(), name="seller_image_delete"),
]