from django.urls import path

from .views import ReviewCreateView

app_name = "reviews"

urlpatterns = [
    path("create/<int:order_item_id>/", ReviewCreateView.as_view(), name="create"),
]