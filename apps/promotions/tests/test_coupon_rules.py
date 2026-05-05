import pytest
from django.utils import timezone
from datetime import timedelta

from apps.cart.models import Cart
from apps.promotions.services import calculate_coupon_discount, validate_coupon_for_cart
from apps.common.tests.factories import UserFactory
from apps.promotions.models import Coupon, CouponUsage


@pytest.mark.django_db
def test_percent_coupon_discount_calculation():
    coupon = Coupon.objects.create(
        code="SALE10",
        discount_type=Coupon.DiscountType.PERCENT,
        value=10,
        min_order_amount=0,
        starts_at=timezone.now() - timedelta(days=1),
        ends_at=timezone.now() + timedelta(days=1),
        is_active=True,
    )

    discount = calculate_coupon_discount(coupon=coupon, subtotal=1000)

    assert discount == 100


@pytest.mark.django_db
def test_fixed_coupon_discount_calculation():
    coupon = Coupon.objects.create(
        code="FIX100",
        discount_type=Coupon.DiscountType.FIXED,
        value=100,
        min_order_amount=0,
        starts_at=timezone.now() - timedelta(days=1),
        ends_at=timezone.now() + timedelta(days=1),
        is_active=True,
    )

    discount = calculate_coupon_discount(coupon=coupon, subtotal=1000)

    assert discount == 100


@pytest.mark.django_db
def test_expired_coupon_should_fail_validation():
    user = UserFactory()
    cart = Cart.objects.create(user=user)

    coupon = Coupon.objects.create(
        code="OLD",
        discount_type=Coupon.DiscountType.PERCENT,
        value=10,
        min_order_amount=0,
        starts_at=timezone.now() - timedelta(days=10),
        ends_at=timezone.now() - timedelta(days=1),
        is_active=True,
    )

    with pytest.raises(ValueError):
        validate_coupon_for_cart(
            user=user,
            code=coupon.code,
            cart=cart,
        )


@pytest.mark.django_db
def test_coupon_min_order_amount_should_fail():
    user = UserFactory()
    cart = Cart.objects.create(user=user)

    coupon = Coupon.objects.create(
        code="MIN1000",
        discount_type=Coupon.DiscountType.PERCENT,
        value=10,
        min_order_amount=1000,
        starts_at=timezone.now() - timedelta(days=1),
        ends_at=timezone.now() + timedelta(days=1),
        is_active=True,
    )

    with pytest.raises(ValueError):
        validate_coupon_for_cart(
            user=user,
            code=coupon.code,
            cart=cart,
        )


@pytest.mark.django_db
def test_coupon_per_user_limit_should_fail():
    user = UserFactory()
    cart = Cart.objects.create(user=user)

    coupon = Coupon.objects.create(
        code="ONEUSE",
        discount_type=Coupon.DiscountType.PERCENT,
        value=10,
        min_order_amount=0,
        per_user_limit=1,
        starts_at=timezone.now() - timedelta(days=1),
        ends_at=timezone.now() + timedelta(days=1),
        is_active=True,
    )

    CouponUsage.objects.create(
        coupon=coupon,
        user=user,
        order_id=1,
    )

    with pytest.raises(ValueError):
        validate_coupon_for_cart(
            user=user,
            code=coupon.code,
            cart=cart,
        )