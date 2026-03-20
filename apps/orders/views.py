from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.users.models import Address

from .services import create_order_from_cart


#***********************
#   🛒 Checkout page
#***********************
class CheckoutView(LoginRequiredMixin, View):
    template_name = "orders/checkout.html"

    def get(self, request):
        addresses = request.user.addresses.all()

        return render(
            request,
            self.template_name,
            {"addresses": addresses},
        )

    def post(self, request):

        shipping_id = request.POST.get("shipping_address")
        billing_id = request.POST.get("billing_address")

        shipping = Address.objects.get(id=shipping_id, user=request.user)
        billing = Address.objects.get(id=billing_id, user=request.user)

        try:
            order = create_order_from_cart(
                request.user,
                shipping,
                billing,
            )

            messages.success(request, "Order created successfully")
            return redirect("orders:detail", order_id=order.id)

        except ValueError as e:
            messages.error(request, str(e))
            return redirect("cart:detail")


#***************************
#   📄 Order Detail View
#***************************
class OrderDetailView(LoginRequiredMixin, View):
    template_name = "orders/order_detail.html"

    def get(self, request, order_id):
        order = request.user.orders.get(id=order_id)

        return render(
            request,
            self.template_name,
            {"order": order},
        )










