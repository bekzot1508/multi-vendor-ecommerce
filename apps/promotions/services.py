from django.utils import timezone

from .models import Coupon, CouponUsage


#************************
#   Coupon validation
#************************
def validate_coupon_for_cart(user, cart, code):

    try:
        coupon = Coupon.objects.get(code=code, is_active=True)
    except Coupon.DoesNotExist:
        raise ValueError("Invalid coupon code")

    now = timezone.now()

    if not (coupon.starts_at <= now <= coupon.ends_at):
        raise ValueError("Coupon expired or not yet active")

    subtotal = sum(item.line_total() for item in cart.items.all())

    if subtotal < coupon.min_order_amount:
        raise ValueError("Minimum order amount not met")

    if coupon.usage_limit is not None:
        if coupon.usages.count() >= coupon.usage_limit:
            raise ValueError("Coupon usage limit reached")

    if coupon.per_user_limit is not None:
        user_usage = coupon.usages.filter(user=user).count()
        if user_usage >= coupon.per_user_limit:
            raise ValueError("You have already used this coupon")

    return coupon


#**************************
#   Discount calculation
#**************************
def calculate_coupon_discount(coupon, subtotal):

    if coupon.discount_type == Coupon.DiscountType.FIXED:
        discount = coupon.value

    else:  # percentage
        discount = subtotal * (coupon.value / 100)

    if coupon.max_discount_amount:
        discount = min(discount, coupon.max_discount_amount)

    discount = min(discount, subtotal)

    return discount



