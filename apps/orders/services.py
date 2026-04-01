import uuid

from django.db import transaction
from django.utils import timezone


from apps.inventory.services import reserve_stock
from apps.promotions.services import calculate_coupon_discount
from apps.payments.services import create_payment_for_order
from apps.notifications.tasks import create_order_notification_task

from apps.cart.models import Cart
from .models import Order, OrderItem, OrderStatusHistory


#**********************
#   CORE FUNCTION
#**********************
@transaction.atomic
def create_order_from_cart(user, shipping_address, billing_address):

    cart = Cart.objects.select_for_update().get(user=user)

    if not cart.items.exists():
        raise ValueError("Cart is empty")

    subtotal = sum(item.line_total() for item in cart.items.all())

    discount = 0
    if cart.coupon:
        discount = calculate_coupon_discount(cart.coupon, subtotal)

    total = subtotal - discount

    order = Order.objects.create(
        user=user,
        order_number=str(uuid.uuid4())[:10].upper(),
        status=Order.Status.AWAITING_PAYMENT,
        shipping_address_snapshot=str(shipping_address),
        billing_address_snapshot=str(billing_address),
        subtotal=subtotal,
        discount_amount=discount,
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
        )

    cart.items.all().delete()

    OrderStatusHistory.objects.create(
        order=order,
        old_status=Order.Status.PENDING,
        new_status=Order.Status.AWAITING_PAYMENT,
        note="Order created from cart, waiting for payment.",
    )

    create_payment_for_order(order)
    create_order_notification_task.delay(order.id)

    return order