from django.db import models

from apps.common.models import TimeStampedModel
from apps.catalog.models import ProductVariant



#****************************
#   inventory record model
#****************************
class InventoryRecord(TimeStampedModel):
    """
    Har bir ProductVariant uchun yagona inventory yozuvi.
    """

    variant = models.OneToOneField(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="inventory",
    )

    total_stock = models.PositiveIntegerField(default=0)
    reserved_stock = models.PositiveIntegerField(default=0)

    low_stock_threshold = models.PositiveIntegerField(default=5)

    def available_stock(self):
        return self.total_stock - self.reserved_stock

    def __str__(self):
        return f"{self.variant} | total={self.total_stock} reserved={self.reserved_stock}"


#****************************
#   stock movement model
#****************************
class StockMovement(TimeStampedModel):
    """
    Stock o‘zgarishlarining audit logi.
    """

    class ChangeType(models.TextChoices):
        STOCK_IN = "stock_in", "Stock In"
        STOCK_OUT = "stock_out", "Stock Out"
        RESERVE = "reserve", "Reserve"
        RELEASE = "release", "Release"
        ADJUSTMENT = "adjustment", "Adjustment"

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="stock_movements",
    )

    change_type = models.CharField(
        max_length=20,
        choices=ChangeType.choices,
    )

    quantity = models.IntegerField()

    note = models.CharField(max_length=255, blank=True)

    related_order_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Order bilan bog‘liq bo‘lsa ID saqlanadi",
    )

    def __str__(self):
        return f"{self.variant} | {self.change_type} | {self.quantity}"