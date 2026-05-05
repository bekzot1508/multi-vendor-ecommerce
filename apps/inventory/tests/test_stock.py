import pytest

from apps.inventory.services import reserve_stock
from apps.inventory.models import InventoryRecord
from apps.common.tests.factories import VariantFactory, InventoryRecordFactory


@pytest.mark.django_db
def test_inventory_reserve_flow():
    variant = VariantFactory()
    record = InventoryRecordFactory(variant=variant, total_stock=10, reserved_stock=0)

    reserve_stock(variant=variant, quantity=3)

    record.refresh_from_db()

    assert record.reserved_stock == 3

@pytest.mark.django_db
def test_reserve_stock_success():
    variant = VariantFactory()

    record = InventoryRecord.objects.create(
        variant=variant,
        total_stock=10,
        reserved_stock=0,
    )

    reserve_stock(variant=variant, quantity=3)

    record.refresh_from_db()

    assert record.reserved_stock == 3


@pytest.mark.django_db
def test_reserve_stock_not_enough():
    variant = VariantFactory()

    InventoryRecord.objects.create(
        variant=variant,
        total_stock=5,
        reserved_stock=5,
    )

    with pytest.raises(Exception):
        reserve_stock(variant=variant, quantity=1)