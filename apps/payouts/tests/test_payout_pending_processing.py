import pytest

from apps.payouts.models import SellerPayout
from apps.payouts.selectors import get_seller_available_balance
from apps.common.tests.factories import (
    SellerFactory,
    OrderFactory,
    OrderItemFactory,
    PayoutFactory,
    get_or_create_shop_for_seller,
)


@pytest.mark.django_db
def test_pending_payout_is_deducted_from_available_balance():
    seller = SellerFactory()
    shop = get_or_create_shop_for_seller(seller)
    order = OrderFactory(status="paid")

    OrderItemFactory(
        order=order,
        shop=shop,
        variant__product__shop=shop,
        status="delivered",
        line_total=1000,
        unit_price=1000,
        quantity=1,
    )

    PayoutFactory(
        seller=seller,
        amount=400,
        status=SellerPayout.Status.PENDING,
    )

    balance = get_seller_available_balance(seller)

    assert balance == 600


@pytest.mark.django_db
def test_processing_payout_is_deducted_from_available_balance():
    seller = SellerFactory()
    shop = get_or_create_shop_for_seller(seller)
    order = OrderFactory(status="paid")

    OrderItemFactory(
        order=order,
        shop=shop,
        variant__product__shop=shop,
        status="delivered",
        line_total=1200,
        unit_price=1200,
        quantity=1,
    )

    PayoutFactory(
        seller=seller,
        amount=500,
        status=SellerPayout.Status.PROCESSING,
    )

    balance = get_seller_available_balance(seller)

    assert balance == 700