from .models import Review


def get_product_reviews(product):
    return (
        Review.objects
        .select_related("user", "product", "order_item")
        .filter(product=product)
        .order_by("-created_at")
    )