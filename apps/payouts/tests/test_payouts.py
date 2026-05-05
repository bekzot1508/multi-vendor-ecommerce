import pytest

from apps.payouts.services import request_payout
from apps.payouts.selectors import get_seller_available_balance
from tests.factories import OrderItemFactory, SellerFactory


@pytest.mark.django_db
def test_payout_balance_correct():
    seller = SellerFactory()

    OrderItemFactory(
        shop__owner=seller,
        status="delivered",
        line_total=500,
    )

    OrderItemFactory(
        shop__owner=seller,
        status="delivered",
        line_total=500,
    )

    balance = get_seller_available_balance(seller)

    assert balance == 1000


@pytest.mark.django_db
def test_request_payout_reduces_balance():
    seller = SellerFactory()

    OrderItemFactory(
        shop__owner=seller,
        status="delivered",
        line_total=1000,
    )

    payout = request_payout(user=seller)

    assert payout.amount == 1000