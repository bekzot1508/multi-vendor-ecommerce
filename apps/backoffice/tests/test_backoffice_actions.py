import pytest
from django.urls import reverse

from apps.shops.models import Shop,ShopStatus
from apps.common.tests.factories import AdminFactory, SellerFactory, ShopFactory


@pytest.mark.django_db
def test_admin_can_approve_shop(client):
    admin = AdminFactory()
    seller = SellerFactory()
    shop = ShopFactory(owner=seller, status=ShopStatus.PENDING)

    client.force_login(admin)

    response = client.post(
        reverse("backoffice:approve_shop", kwargs={"shop_id": shop.id})
    )

    assert response.status_code == 302

    shop.refresh_from_db()
    assert shop.status == ShopStatus.APPROVED


@pytest.mark.django_db
def test_admin_can_block_shop(client):
    admin = AdminFactory()
    seller = SellerFactory()
    shop = ShopFactory(owner=seller, status=ShopStatus.APPROVED)

    client.force_login(admin)

    response = client.post(
        reverse("backoffice:block_shop", kwargs={"shop_id": shop.id})
    )

    assert response.status_code == 302

    shop.refresh_from_db()
    assert shop.status == ShopStatus.BLOCKED