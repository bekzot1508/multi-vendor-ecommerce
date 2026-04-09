from django.db import transaction
from django.db.models import F

from .models import InventoryRecord, StockMovement



#**************************************
#   STOCK IN (omborga qo‘shish)
#**************************************
def increase_stock(variant, quantity, note=""):
    inventory, _ = InventoryRecord.objects.get_or_create(variant=variant)

    inventory.total_stock = F("total_stock") + quantity
    inventory.save()

    StockMovement.objects.create(
        variant=variant,
        change_type=StockMovement.ChangeType.STOCK_IN,
        quantity=quantity,
        note=note,
    )

#**************************************
#   STOCK RESERVE (checkout oldidan)
#   MUHIM: select_for_update ishlatamiz
#**************************************
@transaction.atomic
def reserve_stock(variant, quantity):
    inventory = (
        InventoryRecord.objects
        .select_for_update()
        .get(variant=variant)
    )

    available = inventory.total_stock - inventory.reserved_stock

    if quantity > available:
        raise ValueError("Not enough stock available")

    inventory.reserved_stock = F("reserved_stock") + quantity
    inventory.save()

    StockMovement.objects.create(
        variant=variant,
        change_type=StockMovement.ChangeType.RESERVE,
        quantity=quantity,
    )


#*****************************************
#   RESERVATION RELEASE (payment fail)
#*****************************************
@transaction.atomic
def release_reserved_stock(variant, quantity):
    inventory = (
        InventoryRecord.objects
        .select_for_update()
        .get(variant=variant)
    )

    if quantity > inventory.reserved_stock:
        raise ValueError("Invalid release amount")

    inventory.reserved_stock = F("reserved_stock") - quantity
    inventory.save()

    StockMovement.objects.create(
        variant=variant,
        change_type=StockMovement.ChangeType.RELEASE,
        quantity=quantity,
    )


#*****************************************
#   FINALIZE STOCK (payment success)
#*****************************************
@transaction.atomic
def finalize_reserved_stock(variant, quantity):
    inventory = (
        InventoryRecord.objects
        .select_for_update()
        .get(variant=variant)
    )

    if quantity > inventory.reserved_stock:
        raise ValueError("Invalid finalize amount")

    inventory.total_stock = F("total_stock") - quantity
    inventory.reserved_stock = F("reserved_stock") - quantity
    inventory.save()

    StockMovement.objects.create(
        variant=variant,
        change_type=StockMovement.ChangeType.STOCK_OUT,
        quantity=quantity,
    )


@transaction.atomic
def set_inventory_stock(*, variant, total_stock, low_stock_threshold, note=""):
    """
    Inventory ni aniq qiymatga set qiladi.
    Seller panelda manual stock correction uchun ishlatiladi.

    total_stock:
    - reserved_stock dan kichik bo'lmasligi kerak
    """

    inventory, _ = InventoryRecord.objects.select_for_update().get_or_create(
        variant=variant
    )

    if total_stock < inventory.reserved_stock:
        raise ValueError("Total stock cannot be less than reserved stock")

    old_total_stock = inventory.total_stock
    difference = total_stock - old_total_stock

    inventory.total_stock = total_stock
    inventory.low_stock_threshold = low_stock_threshold
    inventory.save(
        update_fields=["total_stock", "low_stock_threshold", "updated_at"]
    )

    if difference != 0:
        StockMovement.objects.create(
            variant=variant,
            change_type=StockMovement.ChangeType.ADJUSTMENT,
            quantity=difference,
            note=note or "Manual stock adjustment from seller panel",
        )

    return inventory