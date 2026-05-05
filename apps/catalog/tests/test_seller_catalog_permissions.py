import pytest
from django.urls import reverse

from apps.common.tests.factories import SellerFactory, ShopFactory, ProductFactory
from apps.common.tests.factories import get_or_create_shop_for_seller


@pytest.mark.django_db
def test_seller_cannot_edit_other_sellers_product(client):
    seller1 = SellerFactory()

    shop1 = ShopFactory(owner=seller1)
    product = ProductFactory(shop=shop1)

    seller2 = SellerFactory()
    get_or_create_shop_for_seller(seller2)
    client.force_login(seller2)

    response = client.get(
        reverse("catalog:seller_product_edit", kwargs={"pk": product.pk})
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_seller_cannot_delete_other_sellers_product(client):
    seller1 = SellerFactory()
    seller2 = SellerFactory()

    shop1 = ShopFactory(owner=seller1)
    product = ProductFactory(shop=shop1)

    client.force_login(seller2)

    response = client.post(
        reverse("catalog:seller_product_delete", kwargs={"pk": product.pk})
    )

    assert response.status_code == 404