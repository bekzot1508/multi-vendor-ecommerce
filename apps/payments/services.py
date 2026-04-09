import uuid

from django.db import transaction
from django.utils import timezone

from apps.inventory.services import finalize_reserved_stock, release_reserved_stock
from apps.orders.models import Order,OrderItem, OrderStatusHistory
from apps.notifications.tasks import (
    create_order_notification_task,
    create_payment_failed_notification_task,
    create_payment_success_notification_task,
)

from .models import Payment, PaymentCallbackLog, PaymentTransaction


#**********************
#   Payment yaratish
#**********************
def create_payment_for_order(order):
    """
    Har bir order uchun bitta payment.
    Order checkoutdan chiqqach shu yaratiladi.
    """

    if hasattr(order, "payment"):
        return order.payment

    payment = Payment.objects.create(
        order=order,
        external_reference=uuid.uuid4().hex[:16].upper(),
        amount=order.total_amount,
        status=Payment.Status.PENDING,
    )

    PaymentTransaction.objects.create(
        payment=payment,
        transaction_type=PaymentTransaction.TransactionType.INIT,
        amount=payment.amount,
        status=payment.status,
        raw_payload={
            "order_id": order.id,
            "order_number": order.order_number,
            "external_reference": payment.external_reference,
        },
    )

    return payment


#******************************
#   Payment callback process
#******************************
@transaction.atomic
def process_mock_payment_callback(payment, callback_id, action, raw_payload=None):
    """
    action:
    - success
    - fail
    - cancel

    Idempotency:
    shu callback_id oldin ishlangan bo‘lsa, qayta process qilmaymiz.
    """

    raw_payload = raw_payload or {}

    locked_payment = (
        Payment.objects
        .select_for_update()
        .select_related("order")
        .get(id=payment.id)
    )

    callback_log, created = PaymentCallbackLog.objects.get_or_create(
        callback_id=callback_id,
        defaults={
            "payment": locked_payment,
            "raw_payload": {
                "action": action,
                **raw_payload,
            },
            "processed": False,
        },
    )

    if not created:
        return locked_payment

    order = locked_payment.order

    if action == "success":
        if locked_payment.status != Payment.Status.SUCCESS:
            locked_payment.status = Payment.Status.SUCCESS
            locked_payment.save(update_fields=["status", "updated_at"])

        if order.status != Order.Status.PAID:
            old_status = order.status
            order.status = Order.Status.PAID
            order.paid_at = timezone.now()
            order.save(update_fields=["status", "paid_at", "updated_at"])

            OrderStatusHistory.objects.create(
                order=order,
                old_status=old_status,
                new_status=Order.Status.PAID,
                note="Mock payment success callback processed.",
            )

            for item in order.items.select_related("variant"):
                finalize_reserved_stock(item.variant, item.quantity)

        PaymentTransaction.objects.create(
            payment=locked_payment,
            transaction_type=PaymentTransaction.TransactionType.CALLBACK,
            amount=locked_payment.amount,
            status=locked_payment.status,
            raw_payload={
                "callback_id": callback_id,
                "action": action,
                **raw_payload,
            },
        )

        callback_log.processed = True
        callback_log.processed_at = timezone.now()
        callback_log.save(update_fields=["processed", "processed_at", "updated_at"])

        create_payment_success_notification_task.delay(order.id)
        return locked_payment

    if action in ["fail", "cancel"]:
        target_payment_status = (
            Payment.Status.CANCELLED if action == "cancel" else Payment.Status.FAILED
        )

        if locked_payment.status == Payment.Status.SUCCESS:
            return locked_payment

        if locked_payment.status != target_payment_status:
            locked_payment.status = target_payment_status
            locked_payment.save(update_fields=["status", "updated_at"])

        if order.status != Order.Status.PAYMENT_FAILED:
            old_status = order.status
            order.status = Order.Status.PAYMENT_FAILED
            order.save(update_fields=["status", "updated_at"])

            OrderStatusHistory.objects.create(
                order=order,
                old_status=old_status,
                new_status=Order.Status.PAYMENT_FAILED,
                note=f"Mock payment {action} callback processed.",
            )

            for item in order.items.select_related("variant"):
                release_reserved_stock(item.variant, item.quantity)

                # Seller endi bu itemni process qila olmasligi kerak
                if item.status != OrderItem.Status.CANCELLED:
                    item.status = OrderItem.Status.CANCELLED
                    item.save(update_fields=["status", "updated_at"])

        PaymentTransaction.objects.create(
            payment=locked_payment,
            transaction_type=PaymentTransaction.TransactionType.CALLBACK,
            amount=locked_payment.amount,
            status=locked_payment.status,
            raw_payload={
                "callback_id": callback_id,
                "action": action,
                **raw_payload,
            },
        )

        callback_log.processed = True
        callback_log.processed_at = timezone.now()
        callback_log.save(update_fields=["processed", "processed_at", "updated_at"])

        create_payment_failed_notification_task.delay(order.id)
        return locked_payment

    raise ValueError("Invalid payment action")