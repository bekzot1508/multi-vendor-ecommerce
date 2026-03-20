from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedModel


#************************
#   Coupon model
#************************
class Coupon(TimeStampedModel):

    class DiscountType(models.TextChoices):
        FIXED = "fixed", "Fixed amount"
        PERCENT = "percent", "Percentage"

    code = models.CharField(max_length=50, unique=True)

    discount_type = models.CharField(
        max_length=10,
        choices=DiscountType.choices,
    )

    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Amount or percentage",
    )

    min_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    max_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    per_user_limit = models.PositiveIntegerField(null=True, blank=True)

    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


#************************
#   CouponUsage model
#************************
class CouponUsage(TimeStampedModel):
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.CASCADE,
        related_name="usages",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    order_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.coupon.code} used by {self.user_id}"


