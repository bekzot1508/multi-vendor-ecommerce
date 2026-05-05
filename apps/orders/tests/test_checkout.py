import pytest

from apps.orders.services import create_order_from_cart
from apps.cart.services import add_item_to_cart
from apps.inventory.models import InventoryRecord
from apps.users.models import Address
from apps.shipping.models import ShippingMethod
from apps.common.tests.factories import UserFactory, VariantFactory



@pytest.mark.django_db
def test_checkout_creates_order_and_reserves_stock():
    user = UserFactory()
    variant = VariantFactory()

    InventoryRecord.objects.create(
        variant=variant,
        total_stock=10,
        reserved_stock=0,
    )

    add_item_to_cart(user=user, variant=variant, quantity=3)

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

    assert order.items.count() == 1

    record = InventoryRecord.objects.get(variant=variant)

    # 🔥 eng muhim assert
    assert record.reserved_stock == 3

#_______________ Checkout Fail ___________________
@pytest.mark.django_db
def test_checkout_fails_if_stock_not_enough():
    user = UserFactory()
    variant = VariantFactory()

    InventoryRecord.objects.create(
        variant=variant,
        total_stock=2,
        reserved_stock=0,
    )

    with pytest.raises(ValueError):
        add_item_to_cart(user=user, variant=variant, quantity=3)

    with pytest.raises(Exception):
        create_order_from_cart(user=user)
