import pytest

from apps.inventory.models import InventoryRecord
from apps.orders.models import Order
from apps.payments.models import Payment
from apps.payments.services import process_mock_payment_callback
from apps.common.tests.factories import OrderFactory, OrderItemFactory, VariantFactory

@pytest.mark.django_db
def test_fail_then_success_does_not_finalize_again():
    order = OrderFactory(status=Order.Status.AWAITING_PAYMENT)

    variant = VariantFactory()
    InventoryRecord.objects.create(variant=variant, total_stock=10, reserved_stock=2)

    OrderItemFactory(
        order=order,
        variant=variant,
        product=variant.product,
        shop=variant.product.shop,
        quantity=2,
        line_total=200,
        status="pending",
    )

    payment = Payment.objects.create(
        order=order,
        provider_name="mock",
        external_reference="EDGE1",
        amount=200,
        status="pending",
    )

    process_mock_payment_callback(payment, "cb1", "fail")

    # success endi invalid holat
    with pytest.raises(ValueError):
        process_mock_payment_callback(payment, "cb2", "success")