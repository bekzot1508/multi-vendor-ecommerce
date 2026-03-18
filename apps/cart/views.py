from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.catalog.models import ProductVariant

from .services import (
    add_item_to_cart,
    calculate_cart_totals,
    get_or_create_cart,
    remove_cart_item,
    update_cart_item_quantity,
)


#**************************
#   🛒 Cart page
#**************************
class CartDetailView(LoginRequiredMixin, View):
    template_name = "cart/cart_detail.html"

    def get(self, request):
        cart = get_or_create_cart(request.user)
        totals = calculate_cart_totals(cart)

        return render(
            request,
            self.template_name,
            {
                "cart": cart,
                "totals": totals,
            },
        )


#**************************
#   ➕ Add to cart
#**************************
class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, variant_id):
        quantity = int(request.POST.get("quantity", 1))

        variant = ProductVariant.objects.get(id=variant_id)

        try:
            add_item_to_cart(request.user, variant, quantity)
            messages.success(request, "Item added to cart.")
        except ValueError as e:
            messages.error(request, str(e))

        return redirect("cart:detail")


#**************************
#   ✏️ Update quantity
#**************************
class UpdateCartItemView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        quantity = int(request.POST.get("quantity", 1))

        try:
            update_cart_item_quantity(request.user, item_id, quantity)
            messages.success(request, "Cart updated.")
        except ValueError as e:
            messages.error(request, str(e))

        return redirect("cart:detail")


#**************************
#   ❌ Remove item
#**************************
class RemoveCartItemView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        remove_cart_item(request.user, item_id)
        messages.success(request, "Item removed.")

        return redirect("cart:detail")