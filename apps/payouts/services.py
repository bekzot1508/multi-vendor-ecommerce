from django.db import transaction
from django.utils import timezone

from .models import SellerPayout
from .selectors import get_seller_available_balance


@transaction.atomic
def request_payout(user):
    balance = get_seller_available_balance(user)

    if balance <= 0:
        raise ValueError("No available balance")

    payout = SellerPayout.objects.create(
        seller=user,
        amount=balance,
        status=SellerPayout.Status.PENDING,
    )

    return payout


@transaction.atomic
def mark_payout_paid(payout):

    payout.status = SellerPayout.Status.PAID
    payout.paid_at = timezone.now()
    payout.save(update_fields=["status", "paid_at", "updated_at"])

    return payout