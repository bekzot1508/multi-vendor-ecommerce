from django.db.models import Sum

from apps.orders.models import Order, OrderItem


def get_seller_available_balance(user):

    revenue = (
        OrderItem.objects.filter(
            shop__owner=user,
            order__status=Order.Status.PAID,
        )
        .aggregate(total=Sum("line_total"))["total"]
        or 0
    )

    payouts = (
        user.payouts.aggregate(total=Sum("amount"))["total"]
        or 0
    )

    return revenue - payouts