import pytest

from apps.payouts.models import SellerPayout
from apps.payouts.services import mark_payout_paid
from apps.common.tests.factories import SellerFactory, PayoutFactory


@pytest.mark.django_db
def test_admin_marks_payout_paid():
    seller = SellerFactory()

    payout = PayoutFactory(
        seller=seller,
        amount=500,
        status=SellerPayout.Status.PROCESSING,
    )

    mark_payout_paid(payout)

    payout.refresh_from_db()
    assert payout.status == SellerPayout.Status.PAID