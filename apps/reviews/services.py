from django.db import transaction

from apps.orders.models import Order, OrderItem

from .models import Review


@transaction.atomic
def create_review_for_order_item(*, user, order_item, rating, comment=""):
    """
    Rule:
    - only buyer can review
    - only delivered order item can be reviewed
    - one order item = one review
    """

    if order_item.order.user_id != user.id:
        raise ValueError("You cannot review this order item")

    if order_item.status != OrderItem.Status.DELIVERED:
        raise ValueError("You can only review delivered items")

    if hasattr(order_item, "review"):
        raise ValueError("This order item has already been reviewed")

    review = Review.objects.create(
        user=user,
        product=order_item.product,
        order_item=order_item,
        rating=rating,
        comment=comment,
    )

    return review