import pytest

from apps.orders.services import recompute_order_status
from apps.common.tests.factories import OrderFactory, OrderItemFactory


@pytest.mark.django_db
def test_order_not_delivered_if_one_item_only():
    order = OrderFactory(status="paid")

    item1 = OrderItemFactory(order=order, status="delivered")
    item2 = OrderItemFactory(order=order, status="processing")

    recompute_order_status(order)

    order.refresh_from_db()

    assert order.status != "delivered"