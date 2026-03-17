from django.urls import path

from .views import ShopCreateView

app_name = "shops"

urlpatterns = [
    path("create/", ShopCreateView.as_view(), name="create"),
]