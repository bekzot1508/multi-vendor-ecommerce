from django.db import models
from django.utils import timezone

from apps.common.models import TimeStampedModel
from apps.orders.models import Order


class ShippingMethod(TimeStampedModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_days = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["price", "id"]

    def __str__(self):
        return self.name


class Shipment(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PACKED = "packed", "Packed"
        HANDED_TO_COURIER = "handed_to_courier", "Handed to courier"
        IN_TRANSIT = "in_transit", "In transit"
        DELIVERED = "delivered", "Delivered"

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="shipment",
    )
    shipping_method = models.ForeignKey(
        ShippingMethod,
        on_delete=models.PROTECT,
        related_name="shipments",
    )
    tracking_code = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDING,
    )
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def mark_delivered_timestamp(self):
        if self.status == self.Status.DELIVERED and not self.delivered_at:
            self.delivered_at = timezone.now()

    def __str__(self):
        return f"{self.order.order_number} - {self.tracking_code}"