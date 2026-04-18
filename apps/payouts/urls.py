from django.urls import path

from .views import SellerPayoutView

app_name = "payouts"

urlpatterns = [
    path("seller/", SellerPayoutView.as_view(), name="seller"),
]