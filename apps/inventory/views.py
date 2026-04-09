from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.catalog.models import ProductVariant
from apps.users.models import UserRole

from .forms import InventoryUpdateForm
from .models import InventoryRecord, StockMovement
from .services import set_inventory_stock


#***********************************
#   inventory detail/manage view
#***********************************
class SellerInventoryManageView(LoginRequiredMixin, View):
    template_name = "inventory/seller_inventory_manage.html"

    def get(self, request, variant_id):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can manage inventory.")
            return redirect("users:profile")

        variant = get_object_or_404(
            ProductVariant.objects.select_related("product", "product__shop"),
            id=variant_id,
            product__shop__owner=request.user,
        )

        inventory, _ = InventoryRecord.objects.get_or_create(variant=variant)

        form = InventoryUpdateForm(
            initial={
                "total_stock": inventory.total_stock,
                "low_stock_threshold": inventory.low_stock_threshold,
            }
        )

        movements = (
            StockMovement.objects
            .filter(variant=variant)
            .order_by("-created_at")
        )

        return render(
            request,
            self.template_name,
            {
                "variant": variant,
                "inventory": inventory,
                "form": form,
                "movements": movements,
            },
        )

    def post(self, request, variant_id):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can manage inventory.")
            return redirect("users:profile")

        variant = get_object_or_404(
            ProductVariant.objects.select_related("product", "product__shop"),
            id=variant_id,
            product__shop__owner=request.user,
        )

        inventory, _ = InventoryRecord.objects.get_or_create(variant=variant)

        form = InventoryUpdateForm(request.POST)

        if form.is_valid():
            try:
                inventory = set_inventory_stock(
                    variant=variant,
                    total_stock=form.cleaned_data["total_stock"],
                    low_stock_threshold=form.cleaned_data["low_stock_threshold"],
                    note=form.cleaned_data["note"],
                )
                messages.success(request, "Inventory updated successfully.")
                return redirect("inventory:seller_manage", variant_id=variant.id)
            except ValueError as e:
                messages.error(request, str(e))

        movements = (
            StockMovement.objects
            .filter(variant=variant)
            .order_by("-created_at")
        )

        return render(
            request,
            self.template_name,
            {
                "variant": variant,
                "inventory": inventory,
                "form": form,
                "movements": movements,
            },
        )