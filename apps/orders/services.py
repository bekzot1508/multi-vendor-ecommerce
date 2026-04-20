import uuid

from django.db import transaction
from django.utils import timezone

from apps.inventory.services import reserve_stock
from apps.promotions.services import calculate_coupon_discount
from apps.payments.services import create_payment_for_order
from apps.shipping.services import create_shipment_for_order
from apps.notifications.tasks import create_order_notification_task, send_order_created_email

from apps.cart.models import Cart
from .models import Order, OrderItem, OrderStatusHistory


#************************************
#   ORDER STATUS RECOMPUTE HELPER
#************************************
def recompute_order_status(order, changed_by=None, note=""):
    """
    Order statusni itemlar + shipment + payment holatidan qayta hisoblaydi.
    Source of truth:
    - payment failure => payment_failed
    - shipment delivered + all items delivered => delivered
    - shipment in transit / handed to courier => shipped
    - any item processing/packed/shipped => processing yoki shipped
    - paid order default => paid
    """

    old_status = order.status
    new_status = old_status

    if hasattr(order, "payment") and order.payment.status in ["failed", "cancelled"]:
        new_status = Order.Status.PAYMENT_FAILED

    elif hasattr(order, "shipment") and order.shipment.status == "delivered":
        all_items_delivered = not order.items.exclude(
            status=OrderItem.Status.DELIVERED
        ).exists()

        if all_items_delivered:
            new_status = Order.Status.DELIVERED
        else:
            new_status = Order.Status.SHIPPED

    elif hasattr(order, "shipment") and order.shipment.status in [
        "handed_to_courier",
        "in_transit",
    ]:
        new_status = Order.Status.SHIPPED

    elif order.items.filter(
        status__in=[
            OrderItem.Status.PROCESSING,
            OrderItem.Status.PACKED,
            OrderItem.Status.SHIPPED,
        ]
    ).exists():
        new_status = Order.Status.PROCESSING

    elif old_status not in [Order.Status.AWAITING_PAYMENT, Order.Status.PAYMENT_FAILED]:
        new_status = Order.Status.PAID

    if new_status != old_status:
        order.status = new_status
        order.save(update_fields=["status", "updated_at"])

        OrderStatusHistory.objects.create(
            order=order,
            old_status=old_status,
            new_status=new_status,
            changed_by=changed_by,
            note=note or "Order status recomputed from item/shipment state.",
        )

    return order



#**********************
#   CORE FUNCTION
#**********************
@transaction.atomic
def create_order_from_cart(user, shipping_address, billing_address, shipping_method):

    cart = Cart.objects.select_for_update().get(user=user)

    if not cart.items.exists():
        raise ValueError("Cart is empty")

    subtotal = sum(item.line_total() for item in cart.items.all())

    discount = 0
    if cart.coupon:
        discount = calculate_coupon_discount(cart.coupon, subtotal)

    shipping_amount = shipping_method.price
    total = subtotal - discount + shipping_amount

    order = Order.objects.create(
        user=user,
        order_number=str(uuid.uuid4())[:10].upper(),
        status=Order.Status.AWAITING_PAYMENT,
        shipping_address_snapshot=str(shipping_address),
        billing_address_snapshot=str(billing_address),
        subtotal=subtotal,
        discount_amount=discount,
        shipping_amount=shipping_amount,
        total_amount=total,
        placed_at=timezone.now(),
    )

    for item in cart.items.select_related("variant__product__shop"):

        reserve_stock(item.variant, item.quantity)

        OrderItem.objects.create(
            order=order,
            shop=item.variant.product.shop,
            product=item.variant.product,
            variant=item.variant,
            product_name_snapshot=item.variant.product.name,
            variant_name_snapshot=item.variant.name,
            sku_snapshot=item.variant.sku,
            quantity=item.quantity,
            unit_price=item.unit_price,
            line_total=item.line_total(),
            status=OrderItem.Status.PENDING,
        )

    cart.items.all().delete()

    OrderStatusHistory.objects.create(
        order=order,
        old_status=Order.Status.PENDING,
        new_status=Order.Status.AWAITING_PAYMENT,
        note="Order created from cart, waiting for payment.",
    )

    create_payment_for_order(order)
    create_shipment_for_order(order=order, shipping_method=shipping_method)
    create_order_notification_task.delay(order.id)
    send_order_created_email.delay(order.user.email, order.order_number,)

    return order


#**************************************
#  Seller item status update service
#**************************************
@transaction.atomic
def update_seller_order_item_status(*, seller_user, order_item, new_status):
    """
    Seller faqat o'z shopiga tegishli order itemni yangilay oladi.
    Delivered order/item flow erta muzlab qolmasligi kerak.
    """

    if order_item.shop.owner_id != seller_user.id:
        raise ValueError("You cannot manage this order item")

    if order_item.order.status in [
        Order.Status.AWAITING_PAYMENT,
        Order.Status.PAYMENT_FAILED,
        Order.Status.CANCELLED,
    ]:
        raise ValueError("This order item cannot be updated because payment is not completed")

    if order_item.status == OrderItem.Status.CANCELLED:
        raise ValueError("Cancelled order item cannot be updated")

    allowed_statuses = {
        OrderItem.Status.PROCESSING,
        OrderItem.Status.PACKED,
        OrderItem.Status.SHIPPED,
        OrderItem.Status.DELIVERED,
    }

    if new_status not in allowed_statuses:
        raise ValueError("Invalid status")

    # Delivered bo'lgan item qayta orqaga tushmasin
    if order_item.status == OrderItem.Status.DELIVERED and new_status != OrderItem.Status.DELIVERED:
        raise ValueError("Delivered order item cannot be downgraded")

    old_item_status = order_item.status
    order_item.status = new_status
    order_item.save(update_fields=["status", "updated_at"])

    recompute_order_status(
        order_item.order,
        changed_by=seller_user,
        note=f"Seller updated item {order_item.id} from {old_item_status} to {new_status}.",
    )

    return order_item


