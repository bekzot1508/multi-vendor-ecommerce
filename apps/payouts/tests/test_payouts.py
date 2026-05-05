import pytest

from apps.payouts.services import request_payout
from apps.payouts.selectors import get_seller_available_balance
from apps.common.tests.factories import SellerFactory, OrderItemFactory, get_or_create_shop_for_seller, OrderFactory


@pytest.mark.django_db
def test_payout_balance_correct():
    seller = SellerFactory()
    shop = get_or_create_shop_for_seller(seller)

    OrderItemFactory(
        shop=shop,
        variant__product__shop=shop,
        status="delivered",
        line_total=500,
    )

    OrderItemFactory(
        shop=shop,
        variant__product__shop=shop,
        status="delivered",
        line_total=500,
    )

    balance = get_seller_available_balance(seller)

    assert balance == 1000


@pytest.mark.django_db
def test_request_payout_reduces_balance():
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

    payout = request_payout(user=seller)

    assert payout.amount == 1000