from django.db import models
from django.utils import timezone

from apps.common.models import TimeStampedModel


class DailySalesSnapshot(TimeStampedModel):
    """
    Kunlik agregatsiya qilingan savdo metrikalari.
    Celery Beat orqali har kuni yangilanadi.
    """

    date = models.DateField(unique=True)

    total_orders = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    successful_payments = models.PositiveIntegerField(default=0)
    failed_payments = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Snapshot {self.date}"