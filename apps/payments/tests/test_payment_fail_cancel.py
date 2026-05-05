import pytest

from apps.inventory.models import InventoryRecord
from apps.orders.models import Order
from apps.payments.models import Payment
from apps.payments.services import process_mock_payment_callback
from apps.common.tests.factories import OrderFactory, OrderItemFactory, VariantFactory


@pytest.mark.django_db
def test_payment_fail_releases_reserved_stock():
    order = OrderFactory(status=Order.Status.AWAITING_PAYMENT)

    variant = VariantFactory()
    InventoryRecord.objects.create(
        variant=variant,
        total_stock=10,
        reserved_stock=2,
    )

    OrderItemFactory(
        order=order,
        variant=variant,
        product=variant.product,
        shop=variant.product.shop,
        quantity=2,
        unit_price=100,
        line_total=200,
        status="pending",
    )

    payment = Payment.objects.create(
        order=order,
        provider_name="mock_gateway",
        external_reference="FAILPAY1",
        amount=200,
        status=Payment.Status.PENDING,
    )

    process_mock_payment_callback(
        payment=payment,
        callback_id="fail-cb-1",
        action="fail",
        raw_payload={"source": "pytest"},
    )

    payment.refresh_from_db()
    order.refresh_from_db()
    inventory = InventoryRecord.objects.get(variant=variant)

    assert payment.status == Payment.Status.FAILED
    assert order.status == Order.Status.PAYMENT_FAILED
    assert inventory.reserved_stock == 0


@pytest.mark.django_db
def test_payment_cancel_releases_reserved_stock():
    order = OrderFactory(status=Order.Status.AWAITING_PAYMENT)

    variant = VariantFactory()
    InventoryRecord.objects.create(
        variant=variant,
        total_stock=5,
        reserved_stock=1,
    )

    OrderItemFactory(
        order=order,
        variant=variant,
        product=variant.product,
        shop=variant.product.shop,
        quantity=1,
        unit_price=100,
        line_total=100,
        status="pending",
    )

    payment = Payment.objects.create(
        order=order,
        provider_name="mock_gateway",
        external_reference="CANCELPAY1",
        amount=100,
        status=Payment.Status.PENDING,
    )

    process_mock_payment_callback(
        payment=payment,
        callback_id="cancel-cb-1",
        action="cancel",
        raw_payload={"source": "pytest"},
    )

    payment.refresh_from_db()
    order.refresh_from_db()
    inventory = InventoryRecord.objects.get(variant=variant)

    assert payment.status == Payment.Status.CANCELLED
    assert order.status == Order.Status.PAYMENT_FAILED
    assert inventory.reserved_stock == 0