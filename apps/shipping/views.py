from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.orders.models import Order
from apps.users.models import UserRole

from .models import Shipment
from .services import update_shipment_status


#********************************
#   customer shipment detail
#********************************
class ShipmentDetailView(LoginRequiredMixin, View):
    template_name = "shipping/shipment_detail.html"

    def get(self, request, shipment_id):
        shipment = get_object_or_404(
            Shipment.objects.select_related("order", "shipping_method"),
            id=shipment_id,
            order__user=request.user,
        )

        if shipment.order.status in ["awaiting_payment", "payment_failed", "cancelled"]:
            messages.error(request, "Shipment is not available for this order.")
            return redirect("orders:detail", order_id=shipment.order.id)

        return render(request, self.template_name, {"shipment": shipment})


#********************************
#   seller shipment detail
#********************************
class SellerShipmentDetailView(LoginRequiredMixin, View):
    template_name = "shipping/seller_shipment_detail.html"

    def get(self, request, shipment_id):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can access shipment management.")
            return redirect("users:profile")

        shipment = get_object_or_404(
            Shipment.objects.select_related("order", "shipping_method")
            .filter(order__items__shop__owner=request.user)
            .distinct(),
            id=shipment_id,
        )

        if shipment.order.status in ["awaiting_payment", "payment_failed", "cancelled"]:
            messages.error(request, "Shipment is not manageable because payment was not completed.")
            return redirect("orders:seller_item_list")

        return render(request, self.template_name, {"shipment": shipment})


#***********************************
#   seller shipment status update
#***********************************
class SellerShipmentStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, shipment_id):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can update shipments.")
            return redirect("users:profile")

        shipment = get_object_or_404(
            Shipment.objects.select_related("order")
            .filter(order__items__shop__owner=request.user)
            .distinct(),
            id=shipment_id,
        )

        new_status = request.POST.get("status")

        try:
            update_shipment_status(
                shipment=shipment,
                changed_by=request.user,
                new_status=new_status,
            )
            messages.success(request, "Shipment status updated.")
        except ValueError as e:
            messages.error(request, str(e))

        return redirect("shipping:seller_detail", shipment_id=shipment.id)