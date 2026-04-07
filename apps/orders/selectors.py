from .models import OrderItem


def get_seller_order_items(user):
    return (
        OrderItem.objects
        .select_related("order", "product", "variant", "shop")
        .filter(shop__owner=user)
        .order_by("-created_at")
    )