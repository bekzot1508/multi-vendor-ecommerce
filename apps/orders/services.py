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
    """

    if order_item.shop.owner_id != seller_user.id:
        raise ValueError("You cannot manage this order item")

    # Payment qilinmagan yoki payment failed/cancel bo'lgan orderlarni seller boshqarmaydi
    if order_item.order.status in [
        Order.Status.AWAITING_PAYMENT,
        Order.Status.PAYMENT_FAILED,
        Order.Status.CANCELLED,
    ]:
        raise ValueError("This order item cannot be updated because payment is not completed")

    # Cancelled item qayta update qilinmaydi
    if order_item.status == OrderItem.Status.CANCELLED:
        raise ValueError("Cancelled order item cannot be updated")

    if order_item.shop.owner_id != seller_user.id:
        raise ValueError("You cannot manage this order item")

    allowed_statuses = {
        OrderItem.Status.PROCESSING,
        OrderItem.Status.PACKED,
        OrderItem.Status.SHIPPED,
        OrderItem.Status.DELIVERED,
    }

    if new_status not in allowed_statuses:
        raise ValueError("Invalid status")

    old_item_status = order_item.status
    order_item.status = new_status
    order_item.save(update_fields=["status", "updated_at"])

    order = order_item.order

    old_order_status = order.status
    updated_order_status = None

    if new_status == OrderItem.Status.PROCESSING and order.status == Order.Status.PAID:
        updated_order_status = Order.Status.PROCESSING

    elif new_status == OrderItem.Status.SHIPPED and order.status in [Order.Status.PAID, Order.Status.PROCESSING]:
        updated_order_status = Order.Status.SHIPPED

    elif new_status == OrderItem.Status.DELIVERED:
        all_items_delivered = not order.items.exclude(status=OrderItem.Status.DELIVERED).exists()
        if all_items_delivered:
            updated_order_status = Order.Status.DELIVERED

    if updated_order_status and updated_order_status != old_order_status:
        order.status = updated_order_status
        order.save(update_fields=["status", "updated_at"])

        OrderStatusHistory.objects.create(
            order=order,
            old_status=old_order_status,
            new_status=updated_order_status,
            changed_by=seller_user,
            note=f"Seller updated item {order_item.id} from {old_item_status} to {new_status}.",
        )

    return order_item