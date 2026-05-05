import pytest

from apps.orders.services import create_order_from_cart
from apps.payments.services import process_mock_payment_callback
from apps.cart.services import add_item_to_cart
from apps.inventory.models import InventoryRecord
from apps.users.models import Address
from apps.shipping.models import ShippingMethod
from apps.payments.models import Payment
from apps.common.tests.factories import UserFactory, VariantFactory


@pytest.mark.django_db
def test_full_checkout_to_payment_flow():
    user = UserFactory()
    variant = VariantFactory()

    InventoryRecord.objects.create(
        variant=variant,
        total_stock=10,
        reserved_stock=0,
    )

    add_item_to_cart(user=user, variant=variant, quantity=2)

    address = Address.objects.create(
        user=user,
        full_name="Test",
        phone="123",
        country="UZ",
        city="Tashkent",
        area="A",
        line1="Line1",
        postal_code="1000",
    )

    shipping = ShippingMethod.objects.create(
        name="Standard",
        price=10,
        estimated_days=3,
    )

    order = create_order_from_cart(
        user=user,
        shipping_address=address,
        billing_address=address,
        shipping_method=shipping,
    )

    payment = order.payment

    process_mock_payment_callback(
        payment=payment,
        callback_id="abc123",
        action="success",
    )

    order.refresh_from_db()
    payment.refresh_from_db()
    record = InventoryRecord.objects.get(variant=variant)

    assert order.status == "paid"
    assert payment.status == "success"

    # 🔥 FINAL CHECK
    assert record.total_stock == 8
    assert record.reserved_stock == 0