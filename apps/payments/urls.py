from django.urls import path

from .views import MockPaymentActionView, MockPaymentPageView

app_name = "payments"

urlpatterns = [
    path("mock/<int:payment_id>/", MockPaymentPageView.as_view(), name="mock_page"),
    path("mock/<int:payment_id>/action/", MockPaymentActionView.as_view(), name="mock_action"),
]