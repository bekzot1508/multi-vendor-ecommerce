import pytest

from apps.orders.models import Order, OrderItem
from apps.orders.services import recompute_order_status
from apps.shipping.models import Shipment, ShippingMethod
from apps.common.tests.factories import OrderFactory, OrderItemFactory


@pytest.mark.django_db
def test_order_becomes_shipped_when_shipment_in_transit():
    order = OrderFactory(status=Order.Status.PAID)

    shipping_method = ShippingMethod.objects.create(
        name="Standard",
        price=10,
        estimated_days=3,
        is_active=True,
    )

    Shipment.objects.create(
        order=order,
        shipping_method=shipping_method,
        tracking_code="TRK-RECOMP-1",
        status=Shipment.Status.IN_TRANSIT,
    )

    OrderItemFactory(order=order, status=OrderItem.Status.SHIPPED)
    OrderItemFactory(order=order, status=OrderItem.Status.PROCESSING)

    recompute_order_status(order)

    order.refresh_from_db()

    assert order.status == Order.Status.SHIPPED


@pytest.mark.django_db
def test_order_becomes_delivered_only_when_all_items_and_shipment_delivered():
    order = OrderFactory(status=Order.Status.SHIPPED)

    shipping_method = ShippingMethod.objects.create(
        name="Express",
        price=20,
        estimated_days=1,
        is_active=True,
    )

    Shipment.objects.create(
        order=order,
        shipping_method=shipping_method,
        tracking_code="TRK-RECOMP-2",
        status=Shipment.Status.DELIVERED,
    )

    OrderItemFactory(order=order, status=OrderItem.Status.DELIVERED)
    OrderItemFactory(order=order, status=OrderItem.Status.DELIVERED)

    recompute_order_status(order)

    order.refresh_from_db()

    assert order.status == Order.Status.DELIVERED