import pytest
from django.urls import reverse

from apps.common.tests.factories import SellerFactory, ProductFactory, VariantFactory, get_or_create_shop_for_seller


@pytest.mark.django_db
def test_seller_cannot_edit_other_variant(client):
    seller1 = SellerFactory()
    seller2 = SellerFactory()

    shop1 = get_or_create_shop_for_seller(seller1)
    get_or_create_shop_for_seller(seller2)

    product = ProductFactory(shop=shop1)
    variant = VariantFactory(product=product)

    client.force_login(seller2)

    response = client.get(
        reverse("catalog:seller_variant_edit", kwargs={"variant_id": variant.pk})
    )

    assert response.status_code == 404