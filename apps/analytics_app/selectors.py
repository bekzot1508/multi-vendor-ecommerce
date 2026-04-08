from django.db.models import Count, Sum

from apps.inventory.models import InventoryRecord
from apps.orders.models import Order, OrderItem
from apps.payments.models import Payment


#********************************
#   Admin dashboard metrics
#********************************
def get_admin_dashboard_metrics():
    total_orders = Order.objects.count()

    total_revenue = (
        Order.objects
        .filter(status=Order.Status.PAID)
        .aggregate(total=Sum("total_amount"))["total"]
        or 0
    )

    successful_payments = Payment.objects.filter(
        status=Payment.Status.SUCCESS
    ).count()

    failed_payments = Payment.objects.filter(
        status=Payment.Status.FAILED
    ).count()

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "successful_payments": successful_payments,
        "failed_payments": failed_payments,
    }


#********************************
#   Seller dashboard metrics
#********************************
def get_seller_dashboard_metrics(user):
    seller_items = OrderItem.objects.filter(shop__owner=user)

    total_orders = seller_items.count()

    revenue = (
        seller_items
        .filter(order__status=Order.Status.PAID)
        .aggregate(total=Sum("line_total"))["total"]
        or 0
    )

    top_products = (
        seller_items
        .values("product_name_snapshot")
        .annotate(total_qty=Sum("quantity"))
        .order_by("-total_qty")[:5]
    )

    return {
        "total_orders": total_orders,
        "revenue": revenue,
        "top_products": top_products,
    }



#********************************
#   Low stock list
#********************************
def get_low_stock_products():
    return (
        InventoryRecord.objects
        .select_related("variant__product")
        .filter(total_stock__lte=models.F("low_stock_threshold"))
    )



