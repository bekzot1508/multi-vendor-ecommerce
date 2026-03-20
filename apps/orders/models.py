from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedModel
from apps.catalog.models import Product, ProductVariant
from apps.shops.models import Shop


#**********************
#   Order model
#**********************
class Order(TimeStampedModel):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        AWAITING_PAYMENT = "awaiting_payment", "Awaiting payment"
        PAID = "paid", "Paid"
        PROCESSING = "processing", "Processing"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"
        PAYMENT_FAILED = "payment_failed", "Payment failed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    order_number = models.CharField(max_length=20, unique=True)

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDING,
    )

    shipping_address_snapshot = models.TextField()
    billing_address_snapshot = models.TextField()

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    placed_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.order_number


#**********************
#   OrderItem model
#**********************
class OrderItem(TimeStampedModel):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
    )

    product_name_snapshot = models.CharField(max_length=255)
    variant_name_snapshot = models.CharField(max_length=255)
    sku_snapshot = models.CharField(max_length=100)

    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name_snapshot} x {self.quantity}"


#*************************
#   Status History model
#*************************
class OrderStatusHistory(TimeStampedModel):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="status_history",
    )

    old_status = models.CharField(max_length=30)
    new_status = models.CharField(max_length=30)

    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    note = models.CharField(max_length=255, blank=True)








