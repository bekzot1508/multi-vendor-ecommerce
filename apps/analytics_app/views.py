from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from apps.backoffice.mixins import BackofficeAccessMixin

from apps.users.models import UserRole

from .selectors import (
    get_admin_dashboard_metrics,
    get_seller_dashboard_metrics,
    get_seller_sales,
)


#********************************
#   Admin dashboard
#********************************
class AdminDashboardView(BackofficeAccessMixin, View):
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


#********************************
#   Seller Sales View
#********************************
class SellerSalesView(LoginRequiredMixin, View):
    template_name = "analytics/seller_sales.html"

    def get(self, request):
        if request.user.role != UserRole.SELLER:
            return redirect("home")

        start_date = request.GET.get("start")
        end_date = request.GET.get("end")

        sales = get_seller_sales(
            request.user,
            start_date=start_date,
            end_date=end_date,
        )

        return render(
            request,
            self.template_name,
            {
                "sales": sales,
                "start": start_date,
                "end": end_date,
            },
        )