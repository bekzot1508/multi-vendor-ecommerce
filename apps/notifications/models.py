from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedModel


#************************
#   Notification model
#************************
class Notification(TimeStampedModel):
    class Type(models.TextChoices):
        ORDER = "order", "Order"
        PAYMENT = "payment", "Payment"
        STOCK = "stock", "Stock"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=Type.choices)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title


#**********************
#   EmailLog model
#**********************
class EmailLog(TimeStampedModel):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"

    to_email = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING,)
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.to_email} | {self.status}"