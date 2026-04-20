from django.db.models import Sum
from apps.orders.models import OrderItem
from .models import SellerPayout


def get_seller_settled_revenue(user):
    """
    Sellerga haqiqatda settled bo'lgan revenue:
    faqat delivered itemlar.
    """
    return (
        OrderItem.objects.filter(
            shop__owner=user,
            status=OrderItem.Status.DELIVERED,
        ).aggregate(total=Sum("line_total"))["total"]
        or 0
    )


def get_seller_paid_payout_total(user):
    """
    Haqiqatda chiqib ketgan payoutlar.
    """
    return (
        SellerPayout.objects.filter(
            seller=user,
            status=SellerPayout.Status.PAID,
        ).aggregate(total=Sum("amount"))["total"]
        or 0
    )


def get_seller_reserved_payout_total(user):
    """
    Hali to'lanmagan, lekin request qilingan payoutlar.
    Yana bir marta request qilib yubormaslik uchun kerak.
    """
    return (
        SellerPayout.objects.filter(
            seller=user,
            status__in=[
                SellerPayout.Status.PENDING,
                SellerPayout.Status.PROCESSING,
            ],
        ).aggregate(total=Sum("amount"))["total"]
        or 0
    )


def get_seller_available_balance(user):
    """
    Real withdrawable balance:
    delivered revenue
    - paid payouts
    - hali pending/processing payoutlar
    """
    settled_revenue = get_seller_settled_revenue(user)
    paid_payouts = get_seller_paid_payout_total(user)
    reserved_payouts = get_seller_reserved_payout_total(user)

    return settled_revenue - paid_payouts - reserved_payouts