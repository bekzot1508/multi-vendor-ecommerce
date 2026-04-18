from django.urls import path

from .views import (
    ApproveSellerView,
    ApproveShopView,
    BackofficeDashboardView,
    BlockShopView,
    BrandCreateView,
    BrandDeleteView,
    BrandListView,
    BrandUpdateView,
    CategoryCreateView,
    CategoryDeleteView,
    CategoryListView,
    CategoryUpdateView,
    CouponCreateView,
    CouponDeleteView,
    CouponListView,
    CouponUpdateView,
    EmailLogDetailView,
    EmailLogListView,
    LowStockListView,
    NotificationDetailView,
    NotificationListView,
    OrderDetailView,
    OrderListView,
    PaymentDetailView,
    PaymentListView,
    PayoutListView,
    PayoutMarkFailedView,
    PayoutMarkPaidView,
    ProductActivateView,
    ProductDeactivateView,
    ProductDetailView,
    ProductListView,
    RejectSellerView,
    RejectShopView,
    SellerApprovalListView,
    ShippingMethodCreateView,
    ShippingMethodDeleteView,
    ShippingMethodListView,
    ShippingMethodUpdateView,
    ShopListView,
    UserActivateView,
    UserDeactivateView,
    UserDetailView,
    UserListView,
)


app_name = "backoffice"

urlpatterns = [
    path("", BackofficeDashboardView.as_view(), name="dashboard"),
    path("seller-approvals/", SellerApprovalListView.as_view(), name="seller_approvals"),
    path("seller-approvals/<int:profile_id>/approve/", ApproveSellerView.as_view(), name="approve_seller"),
    path("seller-approvals/<int:profile_id>/reject/", RejectSellerView.as_view(), name="reject_seller"),

    path("shops/", ShopListView.as_view(), name="shops"),
    path("shops/<int:shop_id>/approve/", ApproveShopView.as_view(), name="approve_shop"),
    path("shops/<int:shop_id>/reject/", RejectShopView.as_view(), name="reject_shop"),
    path("shops/<int:shop_id>/block/", BlockShopView.as_view(), name="block_shop"),

    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("categories/create/", CategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>/edit/", CategoryUpdateView.as_view(), name="category_update"),
    path("categories/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category_delete"),

    path("brands/", BrandListView.as_view(), name="brand_list"),
    path("brands/create/", BrandCreateView.as_view(), name="brand_create"),
    path("brands/<int:pk>/edit/", BrandUpdateView.as_view(), name="brand_update"),
    path("brands/<int:pk>/delete/", BrandDeleteView.as_view(), name="brand_delete"),

    path("shipping-methods/", ShippingMethodListView.as_view(), name="shipping_method_list"),
    path("shipping-methods/create/", ShippingMethodCreateView.as_view(), name="shipping_method_create"),
    path("shipping-methods/<int:pk>/edit/", ShippingMethodUpdateView.as_view(), name="shipping_method_update"),
    path("shipping-methods/<int:pk>/delete/", ShippingMethodDeleteView.as_view(), name="shipping_method_delete"),

    path("coupons/", CouponListView.as_view(), name="coupon_list"),
    path("coupons/create/", CouponCreateView.as_view(), name="coupon_create"),
    path("coupons/<int:pk>/edit/", CouponUpdateView.as_view(), name="coupon_update"),
    path("coupons/<int:pk>/delete/", CouponDeleteView.as_view(), name="coupon_delete"),

    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/<int:order_id>/", OrderDetailView.as_view(), name="order_detail"),

    path("payments/", PaymentListView.as_view(), name="payment_list"),
    path("payments/<int:payment_id>/", PaymentDetailView.as_view(), name="payment_detail"),

    path("payouts/", PayoutListView.as_view(), name="payout_list"),
    path("payouts/<int:payout_id>/mark-paid/", PayoutMarkPaidView.as_view(), name="payout_mark_paid"),
    path("payouts/<int:payout_id>/mark-failed/", PayoutMarkFailedView.as_view(), name="payout_mark_failed"),

    path("inventory/low-stock/", LowStockListView.as_view(), name="low_stock_list"),

    path("users/", UserListView.as_view(), name="user_list"),
    path("users/<int:user_id>/", UserDetailView.as_view(), name="user_detail"),
    path("users/<int:user_id>/activate/", UserActivateView.as_view(), name="user_activate"),
    path("users/<int:user_id>/deactivate/", UserDeactivateView.as_view(), name="user_deactivate"),

    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<int:product_id>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/<int:product_id>/activate/", ProductActivateView.as_view(), name="product_activate"),
    path("products/<int:product_id>/deactivate/", ProductDeactivateView.as_view(), name="product_deactivate"),

    path("notifications/", NotificationListView.as_view(), name="notification_list"),
    path("notifications/<int:notification_id>/", NotificationDetailView.as_view(), name="notification_detail"),

    path("email-logs/", EmailLogListView.as_view(), name="email_log_list"),
    path("email-logs/<int:email_log_id>/", EmailLogDetailView.as_view(), name="email_log_detail"),
]