from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View

from apps.users.models import Address
from apps.users.models import UserRole
from apps.shipping.models import ShippingMethod
from .models import OrderItem

from .selectors import get_seller_order_items

from .services import create_order_from_cart, update_seller_order_item_status


#***********************
#   🛒 Checkout page
#***********************
class CheckoutView(LoginRequiredMixin, View):
    template_name = "orders/checkout.html"

    def get(self, request):
        addresses = request.user.addresses.all()
        shipping_methods = ShippingMethod.objects.filter(is_active=True)

        return render(
            request,
            self.template_name,
            {
                "addresses": addresses,
                "shipping_methods": shipping_methods,
            },
        )

    def post(self, request):

        shipping_id = request.POST.get("shipping_address")
        billing_id = request.POST.get("billing_address")
        shipping_method_id = request.POST.get("shipping_method")

        shipping = Address.objects.get(id=shipping_id, user=request.user)
        billing = Address.objects.get(id=billing_id, user=request.user)
        shipping_method = ShippingMethod.objects.get(id=shipping_method_id, is_active=True)

        try:
            order = create_order_from_cart(
                user=request.user,
                shipping_address=shipping,
                billing_address=billing,
                shipping_method=shipping_method,
            )

            messages.success(request, "Order created successfully")
            return redirect("payments:mock_page", payment_id=order.payment.id)

        except ValueError as e:
            messages.error(request, str(e))
            return redirect("cart:detail")


#***************************
#   📄 Order Detail View
#***************************
class OrderDetailView(LoginRequiredMixin, View):
    template_name = "orders/order_detail.html"

    def get(self, request, order_id):
        # order = request.user.orders.get(id=order_id)
        order = request.user.orders.select_related("shipment").get(id=order_id)

        return render(
            request,
            self.template_name,
            {"order": order},
        )


#***************************
#   📄 Order list View
#***************************
class OrderListView(LoginRequiredMixin, View):
    template_name = "orders/order_list.html"

    def get(self, request):
        orders = (
            request.user.orders
            .prefetch_related("items")
            .order_by("-created_at")
        )

        return render(
            request,
            self.template_name,
            {"orders": orders},
        )


#============================================================================================
# order managermnet

class SellerOrderItemListView(LoginRequiredMixin, View):
    template_name = "orders/seller_order_item_list.html"

    def get(self, request):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can access this page.")
            return redirect("users:profile")

        items = get_seller_order_items(request.user)

        return render(
            request,
            self.template_name,
            {"items": items},
        )


class SellerOrderItemDetailView(LoginRequiredMixin, View):
    template_name = "orders/seller_order_item_detail.html"

    def get(self, request, item_id):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can access this page.")
            return redirect("users:profile")

        # item = get_object_or_404(
        #     OrderItem.objects.select_related("order", "product", "variant", "shop"),
        #     id=item_id,
        #     shop__owner=request.user,
        # )

        item = get_object_or_404(
            OrderItem.objects.select_related("order", "order__shipment", "product", "variant", "shop"),
            id=item_id,
            shop__owner=request.user,
        )

        return render(
            request,
            self.template_name,
            {"item": item},
        )


class SellerOrderItemStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can update order items.")
            return redirect("users:profile")

        item = get_object_or_404(
            OrderItem.objects.select_related("shop__owner", "order"),
            id=item_id,
            shop__owner=request.user,
        )

        new_status = request.POST.get("status")

        try:
            update_seller_order_item_status(
                seller_user=request.user,
                order_item=item,
                new_status=new_status,
            )
            messages.success(request, "Order item status updated.")
        except ValueError as e:
            messages.error(request, str(e))

        return redirect("orders:seller_item_detail", item_id=item.id)






