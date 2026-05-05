import pytest

from apps.orders.models import Order, OrderItem
from apps.orders.services import update_seller_order_item_status
from apps.common.tests.factories import OrderFactory, OrderItemFactory, SellerFactory, ShopFactory


@pytest.mark.django_db
def test_seller_can_update_only_own_item():
    seller = SellerFactory()
    other_seller = SellerFactory()

    shop = ShopFactory(owner=seller)
    other_shop = ShopFactory(owner=other_seller)

    order = OrderFactory(status=Order.Status.PAID)

    item = OrderItemFactory(
        order=order,
        shop=shop,
        variant__product__shop=shop,
        status=OrderItem.Status.PENDING,
    )

    with pytest.raises(ValueError):
        update_seller_order_item_status(
            seller_user=other_seller,
            order_item=item,
            new_status=OrderItem.Status.PROCESSING,
        )


@pytest.mark.django_db
def test_seller_cannot_update_cancelled_item():
    seller = SellerFactory()
    shop = ShopFactory(owner=seller)
    order = OrderFactory(status=Order.Status.PAID)

    item = OrderItemFactory(
        order=order,
        shop=shop,
        variant__product__shop=shop,
        status=OrderItem.Status.CANCELLED,
    )

    with pytest.raises(ValueError):
        update_seller_order_item_status(
            seller_user=seller,
            order_item=item,
            new_status=OrderItem.Status.PROCESSING,
        )


@pytest.mark.django_db
def test_seller_cannot_downgrade_delivered_item():
    seller = SellerFactory()
    shop = ShopFactory(owner=seller)
    order = OrderFactory(status=Order.Status.PAID)

    item = OrderItemFactory(
        order=order,
        shop=shop,
        variant__product__shop=shop,
        status=OrderItem.Status.DELIVERED,
    )

    with pytest.raises(ValueError):
        update_seller_order_item_status(
            seller_user=seller,
            order_item=item,
            new_status=OrderItem.Status.SHIPPED,
        )


@pytest.mark.django_db
def test_seller_can_update_valid_item_status():
    seller = SellerFactory()
    shop = ShopFactory(owner=seller)
    order = OrderFactory(status=Order.Status.PAID)

    item = OrderItemFactory(
        order=order,
        shop=shop,
        variant__product__shop=shop,
        status=OrderItem.Status.PENDING,
    )

    update_seller_order_item_status(
        seller_user=seller,
        order_item=item,
        new_status=OrderItem.Status.PROCESSING,
    )

    item.refresh_from_db()

    assert item.status == OrderItem.Status.PROCESSING