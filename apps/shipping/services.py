import uuid

from django.db import transaction
from django.utils import timezone

from apps.orders.models import Order, OrderStatusHistory

from .models import Shipment


#********************************
#   shipment yaratish
#********************************
def create_shipment_for_order(*, order, shipping_method):
    if hasattr(order, "shipment"):
        return order.shipment

    tracking_code = f"TRK-{uuid.uuid4().hex[:12].upper()}"

    shipment = Shipment.objects.create(
        order=order,
        shipping_method=shipping_method,
        tracking_code=tracking_code,
        status=Shipment.Status.PENDING,
    )
    return shipment

#********************************
#   shipment status update
#********************************
@transaction.atomic
def update_shipment_status(*, shipment, changed_by, new_status):
    allowed_statuses = {
        Shipment.Status.PENDING,
        Shipment.Status.PACKED,
        Shipment.Status.HANDED_TO_COURIER,
        Shipment.Status.IN_TRANSIT,
        Shipment.Status.DELIVERED,
    }

    if new_status not in allowed_statuses:
        raise ValueError("Invalid shipment status")

    old_shipment_status = shipment.status
    shipment.status = new_status

    if new_status in [Shipment.Status.HANDED_TO_COURIER, Shipment.Status.IN_TRANSIT] and not shipment.shipped_at:
        shipment.shipped_at = timezone.now()

    if new_status == Shipment.Status.DELIVERED and not shipment.delivered_at:
        shipment.delivered_at = timezone.now()

    shipment.save(update_fields=["status", "shipped_at", "delivered_at", "updated_at"])

    order = shipment.order
    old_order_status = order.status
    new_order_status = None

    if new_status in [Shipment.Status.HANDED_TO_COURIER, Shipment.Status.IN_TRANSIT]:
        if order.status in [Order.Status.PAID, Order.Status.PROCESSING]:
            new_order_status = Order.Status.SHIPPED

    elif new_status == Shipment.Status.DELIVERED:
        new_order_status = Order.Status.DELIVERED

    if new_order_status and new_order_status != old_order_status:
        order.status = new_order_status
        order.save(update_fields=["status", "updated_at"])

        OrderStatusHistory.objects.create(
            order=order,
            old_status=old_order_status,
            new_status=new_order_status,
            changed_by=changed_by,
            note=f"Shipment status updated from {old_shipment_status} to {new_status}.",
        )

    return shipment