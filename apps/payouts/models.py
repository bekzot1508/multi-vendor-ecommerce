from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedModel


class SellerPayout(TimeStampedModel):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payouts",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    note = models.TextField(blank=True)

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Payout {self.id} - {self.seller}"