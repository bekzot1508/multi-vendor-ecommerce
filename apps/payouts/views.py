from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.users.models import UserRole

from .selectors import get_seller_available_balance
from .services import request_payout


class SellerPayoutView(LoginRequiredMixin, View):

    template_name = "payouts/seller_payouts.html"

    def get(self, request):

        if request.user.role != UserRole.SELLER:
            return redirect("home")

        balance = get_seller_available_balance(request.user)

        payouts = request.user.payouts.all().order_by("-created_at")

        return render(
            request,
            self.template_name,
            {
                "balance": balance,
                "payouts": payouts,
            },
        )

    def post(self, request):

        try:
            request_payout(request.user)
        except Exception:
            pass

        return redirect("payouts:seller")