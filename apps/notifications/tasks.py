from celery import shared_task

from apps.orders.models import Order

from .models import Notification


@shared_task
def create_order_notification_task(order_id):
    order = Order.objects.select_related("user").get(id=order_id)

    Notification.objects.create(
        user=order.user,
        title="Order created",
        message=f"Your order {order.order_number} has been created.",
        type=Notification.Type.ORDER,
    )


@shared_task
def create_payment_success_notification_task(order_id):
    order = Order.objects.select_related("user").get(id=order_id)

    Notification.objects.create(
        user=order.user,
        title="Payment successful",
        message=f"Payment for order {order.order_number} was successful.",
        type=Notification.Type.PAYMENT,
    )


@shared_task
def create_payment_failed_notification_task(order_id):
    order = Order.objects.select_related("user").get(id=order_id)

    Notification.objects.create(
        user=order.user,
        title="Payment failed",
        message=f"Payment for order {order.order_number} failed or was cancelled.",
        type=Notification.Type.PAYMENT,
    )