import pytest

from apps.orders.models import Order
from apps.orders.services import cancel_order
from apps.common.tests.factories import OrderFactory


@pytest.mark.django_db
def test_order_can_be_cancelled():
    order = OrderFactory(status=Order.Status.PENDING)

    cancel_order(order)

    order.refresh_from_db()
    assert order.status == Order.Status.CANCELLED


@pytest.mark.django_db
def test_paid_order_cannot_be_cancelled():
    order = OrderFactory(status=Order.Status.PAID)

    with pytest.raises(ValueError):
        cancel_order(order)