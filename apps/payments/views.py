import uuid

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .models import Payment
from .services import process_mock_payment_callback


#**********************
#   Mock payment page
#**********************
class MockPaymentPageView(LoginRequiredMixin, View):
    template_name = "payments/mock_payment_page.html"

    def get(self, request, payment_id):
        payment = get_object_or_404(
            Payment.objects.select_related("order"),
            id=payment_id,
            order__user=request.user,
        )

        return render(
            request,
            self.template_name,
            {"payment": payment},
        )


#**********************
#   Mock action view
#**********************
class MockPaymentActionView(LoginRequiredMixin, View):
    def post(self, request, payment_id):
        payment = get_object_or_404(
            Payment.objects.select_related("order"),
            id=payment_id,
            order__user=request.user,
        )

        action = request.POST.get("action")

        if action not in ["success", "fail", "cancel"]:
            messages.error(request, "Invalid action.")
            return redirect("payments:mock_page", payment_id=payment.id)

        callback_id = uuid.uuid4().hex

        try:
            process_mock_payment_callback(
                payment=payment,
                callback_id=callback_id,
                action=action,
                raw_payload={
                    "payment_id": payment.id,
                    "external_reference": payment.external_reference,
                    "user_id": request.user.id,
                },
            )
        except ValueError as e:
            messages.error(request, str(e))
            return redirect("payments:mock_page", payment_id=payment.id)

        if action == "success":
            messages.success(request, "Payment successful.")
        elif action == "fail":
            messages.error(request, "Payment failed.")
        else:
            messages.info(request, "Payment cancelled.")

        return redirect("orders:detail", order_id=payment.order.id)


