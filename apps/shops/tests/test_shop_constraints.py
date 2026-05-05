import pytest
from django.db import IntegrityError

from apps.common.tests.factories import SellerFactory, ShopFactory


@pytest.mark.django_db
def test_one_seller_cannot_have_two_shops():
    seller = SellerFactory()

    ShopFactory(owner=seller)

    with pytest.raises(IntegrityError):
        ShopFactory(owner=seller)