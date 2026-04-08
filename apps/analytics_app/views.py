from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from apps.users.models import UserRole

from .selectors import (
    get_admin_dashboard_metrics,
    get_seller_dashboard_metrics,
)


#********************************
#   Admin dashboard
#********************************
class AdminDashboardView(LoginRequiredMixin, View):
    template_name = "analytics/admin_dashboard.html"

    def get(self, request):

        if request.user.role != UserRole.ADMIN:
            return render(request, "403.html")

        metrics = get_admin_dashboard_metrics()

        return render(
            request,
            self.template_name,
            {"metrics": metrics},
        )


#********************************
#   Seller dashboard
#********************************
class SellerDashboardView(LoginRequiredMixin, View):
    template_name = "analytics/seller_dashboard.html"

    def get(self, request):

        if request.user.role != UserRole.SELLER:
            return render(request, "403.html")

        metrics = get_seller_dashboard_metrics(request.user)

        return render(
            request,
            self.template_name,
            {"metrics": metrics},
        )
