from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedModel
from apps.catalog.models import ProductVariant


#**********************
#   tests model
#**********************
class Cart(TimeStampedModel):
    """
    Har bir user uchun bitta faol tests.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )

    coupon = models.ForeignKey(
        "promotions.Coupon",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Cart of {self.user_id}"


#************************
#   tests item model
#************************
class CartItem(TimeStampedModel):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )

    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        unique_together = ("cart", "variant")

    def line_total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.variant} x {self.quantity}"










