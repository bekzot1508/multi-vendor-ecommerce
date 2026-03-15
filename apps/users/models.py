from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.common.models import TimeStampedModel


class UserRole(models.TextChoices):
    CUSTOMER = "customer", "Customer"
    SELLER = "seller", "Seller"
    ADMIN = "admin", "Admin"


class User(AbstractUser, TimeStampedModel):
    """
    Custom user model.

    Sababi:
    - role qo‘shish oson bo‘ladi
    - keyin auth/business qoidalarni kengaytirish qulay bo‘ladi
    """

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER,
    )

    REQUIRED_FIELDS = ["email", "full_name"]

    def __str__(self):
        return f"{self.username} ({self.role})"


class CustomerProfile(TimeStampedModel):
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="customer_profile",
    )
    phone = models.CharField(max_length=32, blank=True)
    avatar = models.ImageField(upload_to="customers/avatars/", blank=True, null=True)

    def __str__(self):
        return f"CustomerProfile<{self.user_id}>"


class SellerProfile(TimeStampedModel):
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="seller_profile",
    )
    phone = models.CharField(max_length=32, blank=True)
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"SellerProfile<{self.user_id}>"


class Address(TimeStampedModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="addresses",
    )
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=32)
    country = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    area = models.CharField(max_length=128, blank=True)
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=32, blank=True)
    is_default_shipping = models.BooleanField(default=False)
    is_default_billing = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.city}"