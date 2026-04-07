from django.contrib import admin

from .models import Shipment, ShippingMethod


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "estimated_days", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "shipping_method",
        "tracking_code",
        "status",
        "shipped_at",
        "delivered_at",
        "created_at",
    )
    list_filter = ("status", "shipping_method")
    search_fields = ("tracking_code", "order__order_number")