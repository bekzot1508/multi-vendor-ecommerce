import pytest

from apps.inventory.models import InventoryRecord
from apps.orders.models import Order
from apps.payments.models import Payment, PaymentCallbackLog, PaymentTransaction
from apps.payments.services import process_mock_payment_callback
from apps.common.tests.factories import OrderFactory, OrderItemFactory, VariantFactory


@pytest.mark.django_db
def test_second_different_callback_does_not_double_finalize_stock():
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
        external_reference="EDGEPAY1",
        amount=200,
        status=Payment.Status.PENDING,
    )

    process_mock_payment_callback(
        payment=payment,
        callback_id="edge-cb-1",
        action="success",
        raw_payload={"source": "pytest"},
    )

    process_mock_payment_callback(
        payment=payment,
        callback_id="edge-cb-2",
        action="success",
        raw_payload={"source": "pytest"},
    )

    inventory = InventoryRecord.objects.get(variant=variant)
    payment.refresh_from_db()
    order.refresh_from_db()

    assert payment.status == Payment.Status.SUCCESS
    assert order.status == Order.Status.PAID
    assert inventory.total_stock == 8
    assert inventory.reserved_stock == 0
    assert PaymentTransaction.objects.filter(
        payment=payment,
        transaction_type=PaymentTransaction.TransactionType.CALLBACK,
    ).count() == 2


@pytest.mark.django_db
def test_callback_log_created_once_per_callback_id():
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
        external_reference="EDGEPAY2",
        amount=100,
        status=Payment.Status.PENDING,
    )

    process_mock_payment_callback(
        payment=payment,
        callback_id="same-cb-id",
        action="success",
        raw_payload={"source": "pytest"},
    )

    process_mock_payment_callback(
        payment=payment,
        callback_id="same-cb-id",
        action="success",
        raw_payload={"source": "pytest"},
    )

    assert PaymentCallbackLog.objects.filter(callback_id="same-cb-id").count() == 1