from celery import shared_task

from apps.orders.models import Order
from .models import Notification

from .services import send_email_with_log


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


@shared_task
def send_order_created_email(user_email, order_number):

    subject = f"Order {order_number} created"

    body = f"""Your order {order_number} has been successfully created. Thank you for shopping with us."""

    send_email_with_log(
        to_email=user_email,
        subject=subject,
        body=body,
    )


@shared_task
def send_payment_success_email(user_email, order_number):

    subject = f"Payment successful for order {order_number}"

    body = f"""Payment for order {order_number} was successful. Your order is now being processed."""

    send_email_with_log(
        to_email=user_email,
        subject=subject,
        body=body,
    )


@shared_task
def send_payment_failed_email(user_email, order_number):

    subject = f"Payment failed for order {order_number}"

    body = f"""Payment for order {order_number} has failed. Please try again."""

    send_email_with_log(
        to_email=user_email,
        subject=subject,
        body=body,
    )
