import pytest
from apps.common.tests.factories import VariantFactory

from apps.inventory.services import (
    reserve_stock,
    release_reserved_stock,
    finalize_reserved_stock,
)
from apps.inventory.models import InventoryRecord
from apps.common.tests.factories import VariantFactory


@pytest.mark.django_db
def test_reserve_and_release_stock():
    variant = VariantFactory()

    record = InventoryRecord.objects.create(
        variant=variant,
        total_stock=10,
        reserved_stock=0,
    )

    reserve_stock(variant=variant, quantity=4)

    record.refresh_from_db()
    assert record.reserved_stock == 4

    release_reserved_stock(variant=variant, quantity=2)

    record.refresh_from_db()
    assert record.reserved_stock == 2


@pytest.mark.django_db
def test_finalize_stock_after_payment():
    variant = VariantFactory()

    record = InventoryRecord.objects.create(
        variant=variant,
        total_stock=10,
        reserved_stock=3,
    )

    finalize_reserved_stock(variant=variant, quantity=3)

    record.refresh_from_db()

    assert record.total_stock == 7
    assert record.reserved_stock == 0