from django.db import transaction
from django.utils import timezone

from apps.shops.models import Shop, ShopStatus
from apps.users.models import SellerProfile
from apps.payouts.models import SellerPayout
from apps.catalog.models import Product
from apps.users.models import User


@transaction.atomic
def approve_seller_profile(profile):

    profile.is_approved = True
    profile.approved_at = timezone.now()

    profile.save(
        update_fields=["is_approved", "approved_at", "updated_at"]
    )

    return profile


@transaction.atomic
def reject_seller_profile(profile, note=""):

    profile.notes = note
    profile.is_approved = False

    profile.save(update_fields=["notes", "updated_at"])

    return profile


@transaction.atomic
def approve_shop(shop):

    shop.status = ShopStatus.APPROVED

    shop.save(update_fields=["status", "updated_at"])

    return shop


@transaction.atomic
def reject_shop(shop):

    shop.status = ShopStatus.REJECTED

    shop.save(update_fields=["status", "updated_at"])

    return shop


@transaction.atomic
def block_shop(shop):

    shop.status = ShopStatus.BLOCKED

    shop.save(update_fields=["status", "updated_at"])

    return shop


@transaction.atomic
def mark_payout_as_paid(payout):
    payout.status = SellerPayout.Status.PAID
    payout.paid_at = timezone.now()
    payout.save(update_fields=["status", "paid_at", "updated_at"])
    return payout


@transaction.atomic
def mark_payout_as_failed(payout, note=""):
    payout.status = SellerPayout.Status.FAILED
    payout.note = note
    payout.save(update_fields=["status", "note", "updated_at"])
    return payout





@transaction.atomic
def activate_user(user):
    user.is_active = True
    user.save(update_fields=["is_active", "updated_at"])
    return user


@transaction.atomic
def deactivate_user(user):
    user.is_active = False
    user.save(update_fields=["is_active", "updated_at"])
    return user


@transaction.atomic
def activate_product(product):
    product.is_active = True
    product.save(update_fields=["is_active", "updated_at"])
    return product


@transaction.atomic
def deactivate_product(product):
    product.is_active = False
    product.save(update_fields=["is_active", "updated_at"])
    return product

