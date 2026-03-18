from django.contrib import admin

from .models import InventoryRecord, StockMovement


@admin.register(InventoryRecord)
class InventoryRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "variant",
        "total_stock",
        "reserved_stock",
    )
    search_fields = ("variant__sku",)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "variant",
        "change_type",
        "quantity",
        "created_at",
    )
    list_filter = ("change_type",)