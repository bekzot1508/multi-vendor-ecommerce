from django.db import models

from apps.common.models import TimeStampedModel
from apps.orders.models import Order

#**********************
#   Payment model
#**********************
class Payment(TimeStampedModel):
    class Status(models.TextChoices):
        CREATED = "created", "Created"
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"
        REFUNDED = "refunded", "Refunded"

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment",
    )
    provider_name = models.CharField(max_length=50, default="mock_gateway")
    external_reference = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED,
    )

    def __str__(self):
        return f"{self.external_reference} - {self.status}"


#******************************
#   PaymentTransaction model
#******************************
class PaymentTransaction(TimeStampedModel):
    class TransactionType(models.TextChoices):
        INIT = "init", "Init"
        CALLBACK = "callback", "Callback"
        REFUND = "refund", "Refund"

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    raw_payload = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.payment_id} - {self.transaction_type} - {self.status}"


#*******************************
#   PaymentCallbackLog model
#*******************************
class PaymentCallbackLog(TimeStampedModel):
    callback_id = models.CharField(max_length=100, unique=True)
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name="callback_logs",
    )
    raw_payload = models.JSONField()
    processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.callback_id