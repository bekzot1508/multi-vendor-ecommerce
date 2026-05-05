import pytest

from apps.cart.services import add_item_to_cart, update_cart_item_quantity
from apps.inventory.models import InventoryRecord
from apps.common.tests.factories import UserFactory, VariantFactory


@pytest.mark.django_db
def test_add_item_to_cart():
    user = UserFactory()
    variant = VariantFactory()

    InventoryRecord.objects.create(
        variant=variant,
        total_stock=10,
        reserved_stock=0,
    )

    cart_item = add_item_to_cart(user=user, variant=variant, quantity=2)

    assert cart_item.quantity == 2
    assert cart_item.cart.items.count() == 1


@pytest.mark.django_db
def test_cart_quantity_cannot_exceed_stock():
    user = UserFactory()
    variant = VariantFactory()

    InventoryRecord.objects.create(
        variant=variant,
        total_stock=5,
        reserved_stock=0,
    )

    add_item_to_cart(user=user, variant=variant, quantity=3)

    with pytest.raises(Exception):
        update_cart_item_quantity(user=user, variant=variant, quantity=10)