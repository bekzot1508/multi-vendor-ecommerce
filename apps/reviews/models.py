from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedModel
from apps.catalog.models import Product
from apps.orders.models import OrderItem


class Review(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    order_item = models.OneToOneField(
        OrderItem,
        on_delete=models.CASCADE,
        related_name="review",
    )

    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review<{self.product_id}> by {self.user_id}"