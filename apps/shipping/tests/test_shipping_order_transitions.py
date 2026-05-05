import pytest

from apps.orders.models import Order, OrderItem
from apps.orders.services import recompute_order_status
from apps.shipping.models import Shipment, ShippingMethod
from apps.common.tests.factories import OrderFactory, OrderItemFactory


@pytest.mark.django_db
def test_order_does_not_become_delivered_if_shipment_delivered_but_items_not_all_delivered():
    order = OrderFactory(status=Order.Status.SHIPPED)

    shipping_method = ShippingMethod.objects.create(
        name="Standard",
        price=10,
        estimated_days=3,
        is_active=True,
    )

    Shipment.objects.create(
        order=order,
        shipping_method=shipping_method,
        tracking_code="TRK-MIX-1",
        status=Shipment.Status.DELIVERED,
    )

    OrderItemFactory(order=order, status=OrderItem.Status.DELIVERED)
    OrderItemFactory(order=order, status=OrderItem.Status.SHIPPED)

    recompute_order_status(order)
    order.refresh_from_db()

    assert order.status == Order.Status.SHIPPED


@pytest.mark.django_db
def test_order_stays_processing_if_items_processing_and_no_shipment_progress():
    order = OrderFactory(status=Order.Status.PAID)

    shipping_method = ShippingMethod.objects.create(
        name="Slow",
        price=5,
        estimated_days=5,
        is_active=True,
    )

    Shipment.objects.create(
        order=order,
        shipping_method=shipping_method,
        tracking_code="TRK-MIX-2",
        status=Shipment.Status.PENDING,
    )

    OrderItemFactory(order=order, status=OrderItem.Status.PROCESSING)
    OrderItemFactory(order=order, status=OrderItem.Status.PACKED)

    recompute_order_status(order)
    order.refresh_from_db()

    assert order.status == Order.Status.PROCESSING