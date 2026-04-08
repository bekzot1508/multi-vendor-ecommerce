from celery import shared_task
from django.db.models import Sum
from django.utils import timezone

from apps.orders.models import Order
from apps.payments.models import Payment

from .models import DailySalesSnapshot



@shared_task
def generate_daily_sales_snapshot():

    today = timezone.now().date()

    total_orders = Order.objects.filter(
        created_at__date=today
    ).count()

    total_revenue = (
        Order.objects
        .filter(
            created_at__date=today,
            status=Order.Status.PAID,
        )
        .aggregate(total=Sum("total_amount"))["total"]
        or 0
    )

    successful_payments = Payment.objects.filter(
        created_at__date=today,
        status=Payment.Status.SUCCESS,
    ).count()

    failed_payments = Payment.objects.filter(
        created_at__date=today,
        status=Payment.Status.FAILED,
    ).count()

    DailySalesSnapshot.objects.update_or_create(
        date=today,
        defaults={
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "successful_payments": successful_payments,
            "failed_payments": failed_payments,
        },
    )