from django.urls import path

from .views import AdminDashboardView, SellerDashboardView

app_name = "analytics"

urlpatterns = [
    path("admin/", AdminDashboardView.as_view(), name="admin_dashboard"),
    path("seller/", SellerDashboardView.as_view(), name="seller_dashboard"),
]