import pytest

from apps.common.tests.factories import OrderFactory, OrderItemFactory, ProductFactory, UserFactory


@pytest.mark.django_db
def test_only_delivered_item_should_be_reviewable_datawise():
    user = UserFactory()
    product = ProductFactory()
    order = OrderFactory(user=user, status="delivered")

    item = OrderItemFactory(
        order=order,
        product=product,
        variant__product=product,
        shop=product.shop,
        status="delivered",
    )

    assert item.status == "delivered"
    assert item.order.user == user