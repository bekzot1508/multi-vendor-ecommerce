import pytest

from apps.inventory.models import InventoryRecord
from apps.orders.models import Order
from apps.payments.models import Payment, PaymentCallbackLog, PaymentTransaction
from apps.payments.services import process_mock_payment_callback
from apps.common.tests.factories import OrderFactory, OrderItemFactory, VariantFactory


@pytest.mark.django_db
def test_payment_idempotency():
    order = OrderFactory(status=Order.Status.AWAITING_PAYMENT)

    variant = VariantFactory()
    InventoryRecord.objects.create(
        variant=variant,
        total_stock=10,
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
        external_reference="TESTPAY123",
        amount=100,
        status=Payment.Status.PENDING,
    )

    callback_id = "abc123"

    process_mock_payment_callback(
        payment=payment,
        callback_id=callback_id,
        action="success",
        raw_payload={"source": "pytest"},
    )

    process_mock_payment_callback(
        payment=payment,
        callback_id=callback_id,
        action="success",
        raw_payload={"source": "pytest"},
    )

    order.refresh_from_db()
    payment.refresh_from_db()
    inventory = InventoryRecord.objects.get(variant=variant)

    assert payment.status == Payment.Status.SUCCESS
    assert order.status == Order.Status.PAID

    # idempotency: stock faqat 1 marta finalizatsiya bo‘lishi kerak
    assert inventory.total_stock == 9
    assert inventory.reserved_stock == 0

    # callback log ham bitta bo‘lishi kerak
    assert PaymentCallbackLog.objects.filter(callback_id=callback_id).count() == 1

    # init transaction bo‘lmasa ham callback transaction faqat 1 ta yozilishi kerak
    assert PaymentTransaction.objects.filter(
        payment=payment,
        transaction_type=PaymentTransaction.TransactionType.CALLBACK,
    ).count() == 1